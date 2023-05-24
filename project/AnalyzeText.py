import Constant

from typing import Optional

from spacy.tokens import Doc, Span, Token
from spacy import Language

from Model.Action import Action
from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
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


def determine_implicit_marker():
    # todo: algorithm 15 -> TextAnalyzer.java line 1217, not sure whether this is necessary
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

