import Constant

from typing import Optional

from spacy.tokens import Doc, Span, Token
from spacy import Language

from Model.Action import Action
from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
from Structure.Activity import Activity
from Structure.Block import ConditionBlock, AndBlock
from Structure.Structure import LinkedStructure
from Utilities import find_dependency, find_action, contains_indicator


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
        action = find_action(verb, container)
        if action is not None:
            if mark.text.lower() in Constant.SINGLE_IF_CONDITIONAL_INDICATORS:
                action.marker = "if"
            if mark.text.lower() in Constant.SINGLE_ELSE_CONDITIONAL_INDICATORS:
                action.marker = "else"

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
            # elif not advmod.text.lower() == "also":
            #     action.pre_adv_mod = advmod

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

    #
    #         # todo: is this necessary?
    #         for indic in Constant.SEQUENCE_INDICATORS:
    #             if specifier.name.startswith(indic):
    #                 if process.action.pre_adv_mod is None:
    #                     process.action.pre_adv_mod = specifier

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


def construct(container_list: [SentenceContainer]):
    result = []
    for i in range(len(container_list)):
        container = container_list[i]

        if container.has_if() or container.has_else():
            if last_container_has_conditional_marker(container, container_list):
                if isinstance(result[-1], ConditionBlock):
                    result[-1].add_branch(container)
            else:
                if_block = ConditionBlock()
                if_block.add_branch(container)
                result.append(if_block)

        # todo: what if the single sentence contains two parrallel action that has nothing to do with other sentences?
        elif container.has_while():
            if isinstance(result[-1], AndBlock):
                result[-1].add_branch(container)
            elif not isinstance(result[-1], ConditionBlock):
                and_block = AndBlock()
                and_block.add_branch(result[-1])
                and_block.add_branch(container)
                result.remove(result[-1])
                result.append(and_block)

        else:
            result.append(container)

    return result


def build_flows(container_list: [SentenceContainer]):
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
    for container_list in container_list:
        for process in container_list.processes:
            if process.actor is not None:
                if process.actor.is_real_actor and process.actor.full_name not in result:
                    result.append(process.actor.full_name)

    return result


def last_container_has_conditional_marker(container: SentenceContainer, container_list: [SentenceContainer]):
    index = container_list.index(container)
    if index == 0:
        return False
    else:
        if container_list[index - 1].has_if() or container_list[index - 1].has_else():
            return True
        else:
            return False
