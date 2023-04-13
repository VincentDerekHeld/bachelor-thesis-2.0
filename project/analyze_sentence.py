from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


def sentence_finder(sentence):
    result = sub_sentence_finder(sentence)
    if len(result) == 0:
        result = [sentence]
    return result


def sub_sentence_finder(sentence):
    sentence_divider = ["S", "SBAR", "SINV"]
    result = []
    for sub_sentence in sentence._.children:
        # get the label of the sub-sentence when it has one
        label = sub_sentence._.labels[0] if len(sub_sentence._.labels) > 0 else None
        # print(label, "->", sub_sentence)
        if label in sentence_divider:
            result.append(sub_sentence)
    return result


# def determine_sub_sentence_count(sentence):
#     """
#     calculate the number of sub-sentences in a sentence by analyzing the prepositional (PP),
#     adverbial (ADVP), and noun phrases (NP) the sentence contains
#
#     :param str sentence: sentence to be analyzed
#     :return: number of sub-sentences in the sentence
#     :rtype: int
#     """
#     result = count_utils(sentence)
#
#     if result == 1 and sentence[0].tag_ == "WHNP":
#         result -= 1
#
#     for sub_sentence in sentence._.children:
#         label = sub_sentence._.labels[0] if len(sub_sentence._.labels) > 0 else None
#         if label == "PP" or label == "ADVP":
#             result += count_utils(sub_sentence)
#             for sub_sentence_np in sentence._.children:
#                 label_np = sub_sentence_np._.labels[0] if len(sub_sentence_np._.labels) > 0 else None
#                 if label_np == "NP":
#                     result += count_utils(sub_sentence_np)
#
#     # refers to com.inubit.research.textToProcess.transform.AnalyzedSentence -> determineSubSentenceCount
#
#     return result


# def count_utils(sentence):
#     sentence_divider = ["S", "SBAR", "SINV"]
#
#     result = 0
#     for sub_sentence in sentence._.children:
#         # get the label of the sub-sentence when it has one
#         label = sub_sentence._.labels[0] if len(sub_sentence._.labels) > 0 else None
#         # print(label, "->", sub_sentence)
#         if label in sentence_divider:
#             result += 1
#
#     return result


# def analyze_sentence(main_sentence):
#     sentence_count = determine_sub_sentence_count(main_sentence)
#
#     # if the sentence is a simple sentence without any sub-sentences
#     # it is okay to directly perform the elements extraction
#     if sentence_count == 0:
#         extract_elements(main_sentence)
#
#     elif sentence_count == 1:
#         sub_sentence = next(main_sentence._.children)  # todo: this step might be mistaken
#         analyze_sentence(sub_sentence)
#         # todo: find dependency
#
#
#     else:
#         for sub_sentence in main_sentence._.children:
#             analyze_sentence(sub_sentence)


def extract_elements(sentence):
    print("--------------------------------------")
    print("text:", sentence.text)

    sentence_is_active = is_active(sentence)
    print("sentence is active:", sentence_is_active)

    actors = determine_actors(sentence, sentence_is_active)
    print("actors:", actors)

    actions = determine_actions(sentence, sentence_is_active)
    print("actions:", actions)

    objects = determine_objects(actions, sentence_is_active)
    print("objects:", objects)
    print("--------------------------------------")


def is_active(sentence: Doc) -> bool:
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


def determine_actors(sentence: Doc, is_active: bool) -> [Span]:
    """ extract the actors(subjects) of the sentence

        Args:
            sentence: A sentence whose actor(s) should be determined.
            is_active: A boolean value indicating whether the sentence is in active voice or not

        Returns:
            a list of tokens representing the actors of the sentence
    """
    # todo：consider choose a span rather than a token so that all the information of the actor can be extracted
    # The wedding planner is making all the reservations. -> [planner] but should be [(the) wedding planner]
    actors = []
    main_actor = None
    if is_active:
        # find wether the sentence has "nsubj" dependency -> the subject of the sentence
        main_actor = find_dependency("nsubj", sentence)
    else:
        # find wether the sentence has "agent" dependency -> the "by" in the sentence
        agent = find_dependency("agent", sentence)
        if agent is not None:
            main_actor = next(agent.children, None)
        else:
            main_actor = None

    actors.append(get_complete_actor(main_actor))
    # the conjuncts represent the other actors in the sentence and should also be added
    if main_actor is not None and (len(main_actor.conjuncts) > 0):
        for conjunct in main_actor.conjuncts:
            actors.append(get_complete_actor(conjunct))
    return actors


def get_complete_actor(main_actor):
    """ get the complete actor of the sentence

        the sentence "The wedding planner is making all the reservations." has the actor "planner" but should be "the wedding planner"

        Args:
           main_actor: the identified main actor of the sentence

        Returns:
            a list of spans contains the complete actor of the sentence
        """
    if main_actor is None:
        return None

    for child in main_actor.children:
        if child.dep_ == "compound":
            complete_actor = doc[child.left_edge.i:main_actor.i + 1]
            return complete_actor
    return main_actor


def determine_actions(sentence, is_active):
    """extract the actions(verbs) of the sentence

           Args:
               sentence: sentence: A sentence whose action(s) should be determined.
               is_active: A boolean value indicating whether the sentence is in active voice or not

           Returns:
               a list of tokens representing the actors of the sentence
        """
    # todo: refers to com.inubit.research.textToProcess.transform.AnalyzedSentence -> determineVerb function and performed
    #  a excludeRelativeClauses() function. We will skip this step for now because we don't know the meaning of this function.

    predicates = {"main_predicate": None, "sub_predicate": None}
    if is_active:
        verb = find_dependency("nsubj", sentence)
        if verb is not None:
            predicates["main_predicate"] = next(verb.ancestors)
        else:
            verb = find_dependency("dobj", sentence)
            if verb is not None:
                predicates["main_predicate"] = next(verb.ancestors)

        # todo: stanford parser offers a cop relations which can't be identified with spacy, consider whether to implement "cop"
        # NOTE: spacy already gives the correct verb!!!

    else:
        verb = find_dependency("nsubjpass", sentence)
        predicates["main_predicate"] = next(verb.ancestors)

    # todo: determine the verb in the clause（从句） like "If the customer decides that the costs are acceptable"

    if predicates["main_predicate"] is None:
        return None

    # determine the verb in the verb combinations like "decide to withdraw"
    for child in predicates["main_predicate"].children:
        if child.dep_ == "xcomp" or child.dep_ == "acomp":
            predicates["sub_predicate"] = child
            break

    return predicates


def determine_objects(predicates, is_active):
    # todo: might have to be improved
    result = {"objects": [], "whom": []}

    if predicates["sub_predicate"] is not None:
        verb = predicates["sub_predicate"]
    elif predicates["main_predicate"] is not None:
        verb = predicates["main_predicate"]
    else:
        return None

    if is_active:
        for child in verb.children:
            if child.dep_ == "dobj":
                result["objects"].append(child)

        for child in verb.children:
            if child.dep_ == "dative":
                if len(list(child.children)) == 0:
                    result["whom"].append(child)
                else:
                    for sub_child in child.children:
                        if sub_child.dep_ == "pobj":
                            result["whom"].append(sub_child)
    else:
        for child in verb.children:
            if child.dep_ == "nsubjpass":
                result["objects"].append(child)

    return result


def find_dependency(dependency, sentence):
    """find the dependency of the sentence

       Args:
           dependency: A dependency of the sentence
           sentence: A sentence whose voice should be determined.

       Returns:
           the token that has the dependency of the sentence, if no such dependency is found, return None
    """
    for token in sentence:
        if token.dep_ == dependency:
            return token
    return None


if __name__ == '__main__':
    import spacy
    import warnings
    import benepar
    import pyinflect
    import os

    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
    warnings.filterwarnings('ignore')
    nlp = spacy.load('en_core_web_sm')
    # nlp = spacy.load('en_core_web_trf')
    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

    text_input = "The baby was carried by the kangaroo in her pouch. " \
                 "The director will give you the instructions. " \
                 "The video was posted on Facebook by Alex and Nancy. " \
                 "Send the report to the customer. " \
                 "The wedding planner and the action photographer are making all the reservations. " \
                 "The surgeon positions the balloon in an area of blockage and inflates it. " \
                 "If the customer is interested in the product, the salesperson will show him the product. " \
                 "The customers decide to withdraw the money. "
    doc = nlp(text_input)

    for sent in doc.sents:
        sub_sentence_list = sentence_finder(sent)
        for sub_sentence in sub_sentence_list:
            extract_elements(sub_sentence)
