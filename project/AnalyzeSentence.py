import Constant
import spacy

from typing import Optional

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from spacy import Language

from Model.Action import Action
from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
from Utilities import find_dependency, find_action, contains_indicator

from ModelBuilder import create_actor, create_action


# todo: for sentence like The woman who lives next door is a doctor.
#  it will be separated into three sub-sentences. Yet the first and the third is actually one
#  try to identify the "ACTOR" in the first sub-sentence and then check whether it has a nsubj relation with the Verb
#  in the third sub-sentence, if so, combine them into one sub-sentence!
def sub_sentence_finder(sentence: Span, doc: Doc) -> [Span]:
    """find the potential sub-sentences of a sentence, when the sentence has no sub-sentence, return the sentence itself
       in a List.

       Args:
           sentence: The sentence whose sub-sentence must be found
           doc: The document that contains the sentence

       Returns:
           A list of sub-sentences
    """
    sentence_list = find_sub_sentence_start_end_index(sentence, [])
    sentence_list.sort()
    result = []
    symbols = ['.', ',', ';', ':', '!', '?', '(', ')', '[', ']', '{', '}', '"', "'", '``', "''", '“', '”', '‘', '’',
               '—']

    for i in range(len(sentence_list) - 1):
        left = sentence_list[i]
        right = sentence_list[i + 1]
        sentence = doc[left:right]
        if sentence.text in symbols:
            continue
        # if right - left == 1:
        #     if sentence._.labels == ".":
        #         continue
        result.append(sentence)

    return result


def find_sub_sentence_start_end_index(sentence: Span, index_list: [int]):
    """find the start and end index of the sub-sentences

       Args:
           sentence: The sentence whose sub-sentence must be found
           index_list: The list of start and end index of sub-sentences

       Returns:
           A list int number, representing the start and end index of sub-sentences
    """
    labels = sentence._.labels

    if len(labels) == 0:
        return index_list
    elif "SBAR" in labels:
        index_list = add_index(index_list, sentence.start)
        index_list = add_index(index_list, sentence.end)
    elif "S" in labels:
        if sentence._.parent is None:
            index_list = add_index(index_list, sentence.start)
            index_list = add_index(index_list, sentence.end)
        elif not "SBAR" in sentence._.parent._.labels:
            index_list = add_index(index_list, sentence.start)
            index_list = add_index(index_list, sentence.end)

    children = list(sentence._.children)

    for sub_sentence in children:
        find_sub_sentence_start_end_index(sub_sentence, index_list)

    return index_list


def add_index(index_list, index):
    if index in index_list:
        return index_list
    else:
        index_list.append(index)
        return index_list


def analyze_document(nlp: Language, doc: Doc) -> [SentenceContainer]:
    result = []
    for sentence in doc.sents:
        container = SentenceContainer(sentence)
        result.append(container)

        sub_sentence_list = sub_sentence_finder(sentence, doc)
        for sub_sentence in sub_sentence_list:
            process = Process(sub_sentence)
            extract_elements(sub_sentence, process, nlp)
            container.add_process(process)

        if len(container.processes) > 1:
            find_xcomp(container.processes)

    return result


def find_xcomp(processes):
    xcomp = None
    for process in processes:
        if process.action is None:
            continue

        for child in process.action.token.children:
            if child.dep_ == "xcomp":
                xcomp = child
                break

        if xcomp is not None:
            for p in processes:
                if p.action.token == xcomp and p != process:
                    process.action.xcomp = p.action


def extract_elements(sentence, process, nlp: Language):
    sentence_is_active = is_active(nlp, sentence)

    actor = determine_actor(sentence, sentence_is_active)
    process.actor = create_actor(actor)

    verb = determine_predicate(sentence, sentence_is_active)
    obj = determine_object(verb, sentence_is_active)
    process.action = create_action(verb, obj)


def is_active(nlp: Language, sentence: Span) -> bool:
    """ determine whether the sentence is in active or in passive voice

        Args:
            sentence: A sentence whose voice should be determined.

        Returns:
            return True if the sentence is in active voice, False otherwise

        References:
            https://gist.github.com/armsp/30c2c1e19a0f1660944303cf079f831a
    """
    matcher = Matcher(nlp.vocab)
    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('passive', [passive_rule])
    matches = matcher(sentence)
    if len(matches) > 0:
        return False
    else:
        return True


def determine_actor(sentence: Span, active: bool) -> Optional[Token]:
    """ extract the actor(subject) of the sentence

        Args:
            sentence: A sentence whose actor should be determined.
            active: A boolean value indicating whether the sentence is in active voice or not

        Returns:
            if the actor is identified, return it as a token, otherwise return None
    """

    if active:
        # find whether the sentence has "nsubj" dependency -> the subject of the sentence
        search = find_dependency(["nsubj"], sentence=sentence)
        main_actor = search[0] if len(search) > 0 else None
    else:
        # find whether the sentence has "agent" dependency -> the "by" in the sentence
        agent = find_dependency(["agent"], sentence=sentence)
        main_actor = next(agent[0].children) if len(agent) > 0 else None

    return main_actor


def determine_predicate(sentence: Span, active: bool) -> Optional[Token]:
    """extract the verb of the sentence

       Args:
           sentence: sentence: A sentence whose action(s) should be determined.
           active: A boolean value indicating whether the sentence is in active voice or not

       Returns:
           if the verb is identified, return it as a token, otherwise return None
    """

    # predicates = []
    if active:
        actor = find_dependency(["nsubj"], sentence=sentence)
        if len(actor) == 0:
            actor = find_dependency(["dobj"], sentence=sentence)

    else:
        actor = find_dependency(["nsubjpass"], sentence=sentence)

    if len(actor) > 0:
        verb = next(actor[0].ancestors)
        return verb

    return None


def determine_object(predicate: Token, active: bool) -> Optional[Token]:
    """extract the object of the sentence

       Args:
           predicate: The verb in the sentence.
           active: A boolean value indicating whether the sentence is in active voice or not

       Returns:
           if there is a direct object, return it as a token, otherwise return None
    """

    if active:
        if predicate is None:
            return None
        obj = find_dependency(["dobj"], token=predicate)
        if len(obj) == 0:
            obj = find_dependency(["pobj"], token=predicate)

    else:
        obj = find_dependency(["nsubjpass"], token=predicate)

    if len(obj) > 0:
        return obj[0]

    return None


def determine_marker(container: SentenceContainer, nlp: Language):
    has_found_marker = determine_single_marker(container)
    if not has_found_marker:
        determine_compound_marker(container, nlp)


def determine_single_marker(container: SentenceContainer) -> bool:
    found_marker = False

    mark_list = find_dependency(["mark"], sentence=container.sentence)
    for mark in mark_list:
        verb = next(mark.ancestors)
        action = find_action(verb, container)
        if action is not None:
            if mark.text.lower() in Constant.SINGLE_CONDITIONAL_INDICATORS:
                action.marker = "if"
                found_marker = True

    advmod_list = find_dependency(["advmod"], sentence=container.sentence)
    for advmod in advmod_list:
        verb = next(advmod.ancestors)
        action = find_action(verb, container)
        if action is not None:
            if advmod.text.lower() in Constant.SINGLE_PARALLEL_INDICATORS:
                action.marker = "while"
                found_marker = True
            elif advmod.text.lower() in Constant.SINGLE_CONDITIONAL_INDICATORS:
                action.marker = "if"
                found_marker = True
            elif advmod.text.lower() in Constant.SINGLE_SEQUENCE_INDICATORS:
                action.marker = "then"
                found_marker = True
            # elif not advmod.text.lower() == "also":
            #     action.pre_adv_mod = advmod

    prep_list = find_dependency(["prep"], sentence=container.sentence)
    for prep in prep_list:
        verb = next(prep.ancestors)
        action = find_action(verb, container)
        if action is not None:
            action.prep = prep

    return found_marker


def determine_compound_marker(container: SentenceContainer, nlp: Language):
    for process in container.processes:
        if process.action is None:
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


def correct_order(container: [SentenceContainer]) -> [Process]:
    result = []

    for sentence in container:
        for process in sentence.processes:
            if process.action is None:
                continue

            if process.action.marker == "if":
                if not sentence.process_is_first(process):
                    # stop the maneuver if the pressure is too high -> if the pressure is too high, stop the maneuver
                    result.insert(len(result) - 1, process)
                else:
                    result.append(process)
            else:
                result.append(process)

    return result


if __name__ == '__main__':
    import spacy
    import warnings
    import benepar
    import os
    from spacy_wordnet.wordnet_annotator import WordnetAnnotator

    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
    warnings.filterwarnings('ignore')
    A_nlp = spacy.load('en_core_web_sm')
    # nlp = spacy.load('en_core_web_trf')
    A_nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})
    A_nlp.add_pipe("spacy_wordnet", after='tagger')

    # text_input = "Father and mother wrote me, Daisy and Anne a letter." \
    #              "The baby was carried by the kangaroo in her pouch. " \
    #              "The director will give you the instructions. " \
    #              "The video was posted on Facebook by Alex and Nancy. " \
    #              "Send the report to the customer. " \
    #              "The wedding planner and the action photographer are making all the reservations. " \
    #              "The surgeon positions the balloon in an area of blockage and inflates it. " \

    text_input = "In case customer accepts the offer, the salesperson will base on this close the deal. " \
                 "Otherwise, the salesperson will offer a lower price. " \
                 "In the meantime, the customer prepares the payment. " \
                 "subsequently the salesperson delivers the product." \
                 "The process is finished, if the customer is satisfied."

    # text_input = open('Text/text02.txt', 'r').read().replace('\n', ' ')

    document = A_nlp(text_input)
    container = analyze_document(A_nlp, document)
    for cont in container:
        determine_marker(cont, A_nlp)
    acts = correct_order(container)
    for act in acts:
        print("-" * 10)
        marker = act.action.marker
        if marker is not None:
            print(marker + "->")

        actor = act.actor
        action = act.action
        obj = action.object

        if actor is not None:
            print("Actor: "+actor.token.text)
        if action is not None:
            print("Action: "+action.token.text)
        if obj is not None:
            print("Object: "+obj.token.text)

        print("-" * 10)
