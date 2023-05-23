from typing import Optional

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from spacy import Language

from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
from AnalyzeText import determine_marker, correct_order
from Utilities import find_dependency

from ModelBuilder import create_actor, create_action, correct_model


def sub_sentence_finder(sentence: Span) -> [Span]:
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
        sentence = sentence.doc[left:right]
        if sentence.text in symbols:
            continue
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

        sub_sentence_list = sub_sentence_finder(sentence)
        for sub_sentence in sub_sentence_list:
            process = Process(sub_sentence)
            extract_elements(sub_sentence, process, nlp)
            container.add_process(process)

        if len(container.processes) > 1:
            find_xcomp(container.processes)

    for sentence in result:
        correct_model(sentence)

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

    if process.action is not None:
        for conjunct in process.action.token.conjuncts:
            if conjunct == process.action.token:
                continue
            if sentence.start < conjunct.i < sentence.end:
                conjunct_obj = determine_object(conjunct, sentence_is_active)
                conjunct_action = create_action(conjunct, conjunct_obj)
                process.action.conjunction.append(conjunct_action)

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
        obj = find_dependency(["dobj", "acomp"], token=predicate)
        if len(obj) == 0:
            obj = find_dependency(["pobj"], token=predicate)

    else:
        obj = find_dependency(["nsubjpass"], token=predicate)

    if len(obj) > 0:
        return obj[0]

    return None

