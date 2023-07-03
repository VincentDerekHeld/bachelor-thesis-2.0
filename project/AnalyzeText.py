import Constant

from typing import Optional

from spacy.tokens import Doc, Span, Token
from spacy import Language

from Model.Action import Action
from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
from Structure.Activity import Activity
from Structure.Block import ConditionBlock, AndBlock
from Structure.Structure import LinkedStructure, Structure
from Utilities import find_dependency, find_action, contains_indicator, find_process
from WordNetWrapper import hypernyms_checker


def determine_marker(container: SentenceContainer, nlp: Language):
    """
    Determines the marker of the action in the given container.

    Args:
        container: The container that contains the action.
        nlp: The nlp language object.

    """
    determine_single_marker(container)
    determine_compound_marker(container, nlp)


def determine_single_marker(container: SentenceContainer):
    """
    Determines the marker of the action that is composed of one word in the given container.

    Args:
        container: The container that contains the action.

    """
    mark_list = find_dependency(["mark"], sentence=container.sentence)
    for mark in mark_list:
        verb = next(mark.ancestors)
        if verb.pos_ == "PART":
            verb = next(verb.ancestors)
        action = find_action(verb, container)
        if action is not None:
            if mark.text.lower() in Constant.SINGLE_IF_CONDITIONAL_INDICATORS:
                action.marker = "if"
            elif mark.text.lower() in Constant.SINGLE_ELSE_CONDITIONAL_INDICATORS:
                action.marker = "else"
            elif mark.text.lower() == "that":
                if verb.dep_ == "ccomp":
                    main_clause = find_action(next(verb.ancestors), container)
                    if main_clause is not None:
                        sub_clause = find_action(verb, container)
                        sub_clause_process = find_process(container, action=sub_clause)
                        main_clause.subclause = sub_clause_process
                        container.processes.remove(sub_clause_process)

    advmod_list = find_dependency(["advmod"], sentence=container.sentence)
    for advmod in advmod_list:
        verb = next(advmod.ancestors)
        action = find_action(verb, container)
        if action is not None:
            if advmod.text.lower() in Constant.SINGLE_PARALLEL_INDICATORS:
                action.marker = "while"
            elif advmod.text.lower() in Constant.SINGLE_IF_CONDITIONAL_INDICATORS:
                action.marker = "if"
            elif advmod.text.lower() in Constant.SINGLE_ELSE_CONDITIONAL_INDICATORS:
                action.marker = "else"
            elif advmod.text.lower() in Constant.SINGLE_SEQUENCE_INDICATORS:
                action.marker = "then"

    prep_list = find_dependency(["prep"], sentence=container.sentence)
    for prep in prep_list:
        verb = next(prep.ancestors)
        action = find_action(verb, container)
        if action is not None:
            action.prep = prep


def determine_compound_marker(container: SentenceContainer, nlp: Language):
    """
    Determines the marker of the action that is composed of multiple words in the given container.

    Args:
        container: The container that contains the action.
        nlp: The nlp language object.

    """
    for process in container.processes:
        if process.action is None:
            continue

        if process.action.marker is not None:
            continue

        if contains_indicator(Constant.COMPOUND_CONDITIONAL_INDICATORS, process.sub_sentence, nlp):
            process.action.marker = "if"
        elif contains_indicator(Constant.COMPOUND_PARALLEL_INDICATORS, process.sub_sentence, nlp):
            process.action.marker = "while"
        elif contains_indicator(Constant.COMPOUND_SEQUENCE_INDICATORS, process.sub_sentence, nlp):
            process.action.marker = "then"

    return None


def correct_order(container: [SentenceContainer]):
    """
    # stop the maneuver if the pressure is too high -> if the pressure is too high, stop the maneuver

    Args:
        container: The container that contains the action.

    """

    for sentence in container:
        for process in sentence.processes:
            if process.action is None:
                continue

            if process.action.marker == "if":
                if not sentence.process_is_first(process):
                    # stop the maneuver if the pressure is too high -> if the pressure is too high, stop the maneuver
                    # swap the process with the other process that is before it in the container.processes list
                    index = sentence.processes.index(process)
                    sentence.processes.remove(process)
                    sentence.processes.insert(index - 1, process)


def remove_redundant_processes(container: [SentenceContainer]):
    for sentence in container:
        for i in range(len(sentence.processes) - 1, -1, -1):
            if sentence.processes[i].action is None:
                sentence.processes.remove(sentence.processes[i])
            # elif sentence.processes[i].action.token.lemma_ == "be":
            #     acomp = find_dependency(["acomp"], token=sentence.processes[i].action.token)
            #     if len(acomp) == 0:
            #         sentence.processes.remove(sentence.processes[i])


def determine_end_activities(structure_list: [Structure]):
    for structure in structure_list:
        if structure_list.index(structure) == len(structure_list) - 1:
            structure.is_end_activity = True
        elif isinstance(structure, ConditionBlock):
            for branch in structure.branches:
                for activity in branch["actions"]:
                    if activity.process.action.active:
                        actor = activity.process.actor
                    else:
                        actor = activity.process.action.object
                    if actor is not None:
                        if hypernyms_checker(actor.token, ["event"]) and \
                                hypernyms_checker(activity.process.action.token, ["end"]):
                            activity.is_end_activity = True


def construct(container_list: [SentenceContainer]):
    result = []
    for i in range(len(container_list)):
        container = container_list[i]

        if container.has_if() or container.has_else():
            if last_container_has_conditional_marker(container, container_list):
                if isinstance(result[-1], ConditionBlock):
                    if result[-1].can_be_added(container):
                        result[-1].add_branch(container)
                    else:
                        if_block = ConditionBlock()
                        if_block.add_branch(container)
                        result.append(if_block)
            else:
                if_block = ConditionBlock()
                if_block.add_branch(container)
                result.append(if_block)

        elif container.has_while():
            if isinstance(result[-1], AndBlock):
                result[-1].add_branch(container)
            elif not isinstance(result[-1], ConditionBlock):
                and_block = AndBlock()
                and_block.add_branch(result[-1])
                and_block.add_branch(container)
                result.remove(result[-1])
                result.append(and_block)

        elif container.has_or():
            and_block = AndBlock()
            for process in container.or_processes:
                branch = [Activity(process)]
                and_block.branches.append(branch)
            result.append(and_block)

        else:
            result.append(container)

    return result


def build_flows(container_list: [SentenceContainer]):
    flow_list = construct(container_list)
    result = []

    for i in range(len(flow_list)):
        if isinstance(flow_list[i], ConditionBlock):
            if not flow_list[i].is_complete():
                flow_list[i].create_dummy_branch()
            result.append(flow_list[i])
        elif isinstance(flow_list[i], AndBlock):
            result.append(flow_list[i])
        else:
            for process in flow_list[i].processes:
                result.append(Activity(process))

    return result


def build_linked_list(container_list: [SentenceContainer]):
    flow_list = construct(container_list)
    link = LinkedStructure()

    for i in range(len(flow_list)):
        if isinstance(flow_list[i], ConditionBlock):
            link.add_structure(flow_list[i])
            # todo: if the condition gateway has only one branch, we might have to search another to merge.
            # if flow_list[i].is_complete():
            #     link.add_structure(flow_list[i])
            # else:
            #     pass
        elif isinstance(flow_list[i], AndBlock):
            link.add_structure(flow_list[i])
        else:
            for process in flow_list[i].processes:
                activity = Activity(process)
                link.add_structure(activity)

    return link


def get_valid_actors(container_list: [SentenceContainer]):
    result = []
    for container in container_list:
        for process in container.processes:
            if process.actor is not None:
                if process.actor.is_real_actor and process.actor.full_name not in result:
                    result.append(process.actor.full_name)

    return result


def adjust_actors(container_list: [SentenceContainer], valid_actors: [str]):
    for container in container_list:
        for process in container.processes:
            if process.actor is not None and not process.actor.is_real_actor:
                for valid_actor in valid_actors:
                    if process.actor.full_name in valid_actor:
                        process.actor.full_name = valid_actor


def last_container_has_conditional_marker(container: SentenceContainer, container_list: [SentenceContainer]):
    index = container_list.index(container)
    if index == 0:
        return False
    else:
        if container_list[index - 1].has_if() or container_list[index - 1].has_else():
            return True
        else:
            return False
