# from project.AnalyzeSentence import is_active, determine_actor, determine_predicate, determine_object, create_actor, create_action
from typing import Any

import benepar, spacy
from spacy import Language
from spacy.tokens import Span

"""
def extract_elements(sentence, process):
    sentence_is_active = is_active(sentence)

    actor = determine_actor(sentence, sentence_is_active)
    process.actor = create_actor(actor)

    verb = determine_predicate(sentence, sentence_is_active)
    obj = determine_object(verb, sentence_is_active)
    process.action = create_action(verb, obj)




        
"""
subject_dependencies = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
object_dependencies = ["dobj", "dative", "attr", "oprd", "pobj", "iobj", "obj"]


def immediately_dominates(A: Span, B: Span):
    # Check if the parent of B is A
    return B._.parent == A


# Another function to check if A dominates B
def dominates(A: Span, B: Span):
    current = B
    while current._.parent is not None:
        if current._.parent == A:
            return True
        current = current._.parent
    return False


def are_sisters(span_A: Span, span_B: Span):
    # Assuming span_A and span_B are two spans you're comparing
    print("span_A.root.head:", span_A.root.head)
    print("span_B.root.head:", span_B.root.head)
    return span_A.root.head == span_B.root.head


def check_labels(sent, labels):
    """
    Checks if the given labels exist in the constituency parse of the doc.
    Returns a dictionary with the labels and their occurrence status.
    """
    results = {}
    for label in labels:
        results[label] = any(subtree._.labels == label for subtree in sent._.constituents)
    return results


def determine_NP(sent) -> Span:
    for const in sent._.constituents:
        if len(const._.labels) > 0 and const._.labels[0] == 'NP':
            return const


labels = ["MD", "NP", "VP", "IN", "PP", "SBAR", "SINV"]

ACTOR_MARKERS = ("organization", "Organization", "the organization", "The organization")
"""set(["organization", "Organization", "the organization", "The organization",
                 "Actor", "Physician", "expert", "company",
                 "judge", "prosecutor", "driver", "officer",
                 "inspector"
                 ]))"""


def check_for_label_dominating_actor_marker(sent: Span, label: str):  # subject dependency and NP < (actormarker)
    """
    Check if there's a noun phrase (NP) that immediately
    dominates any of the specified actor markers.
    """
    results = []
    print("sent._.constituents", list(sent._.constituents))
    for subtree in sent._.constituents:
        """if len(subtree._.labels) > 0:
            #print("subtree._.labels", subtree._.labels, "len(subtree._.labels) > 0", len(subtree._.labels) > 0, "subtree._.labels[0] == NP ", subtree._.labels[0], "Token:", any(
                token.text in ACTOR_MARKERS for token in subtree).__str__())
        for token in subtree:
            print("Token:", token.text)"""
        if len(subtree._.labels) > 0 and subtree._.labels[0] == label and any(
                token.text in ACTOR_MARKERS for token in subtree):
            results.append(subtree)
    return results


def check_conditions1(sent: Span):  # subject dependency and NP < (actormarker)
    """
    Check if there's a noun phrase (NP) that immediately
    dominates any of the specified actor markers.
    """
    print("sent._.constituents", list(sent._.constituents))
    for subtree in sent._.constituents:
        """if len(subtree._.labels) > 0:
            #print("subtree._.labels", subtree._.labels, "len(subtree._.labels) > 0", len(subtree._.labels) > 0, "subtree._.labels[0] == NP ", subtree._.labels[0], "Token:", any(
                token.text in ACTOR_MARKERS for token in subtree).__str__())
        for token in subtree:
            print("Token:", token.text)"""
        if len(subtree._.labels) > 0 and subtree._.labels[0] == "NP" and any(
                token.text in ACTOR_MARKERS for token in subtree):
            for token in subtree:
                if token.dep_ in subject_dependencies:
                    print("Sentence: ", subtree.text)
                    return True
    return False


def check_conditions2(sent: Span):
    is_object_dependency = any(token.dep_ in ["dobj", "iobj", "obj"] for token in sent)
    is_passive_voice = any(token.dep_ == "auxpass" for token in sent)

    if not (is_object_dependency and is_passive_voice):
        return False

    for constituent in sent._.constituents:
        if constituent.label_ == "PP":
            for child in constituent._.children:
                if child.label_ == "IN":
                    for sibling in child._.siblings:
                        if sibling.label_ == "NP" and any(token.text in ACTOR_MARKERS for token in sibling):
                            return True

    return False


def check_conditions3(doc):
    # Check for object dependency
    is_object_dependency = any(token.dep_ in ["dobj", "iobj", "obj"] for token in doc)

    # Check for active voice (ensure no passive auxiliaries are present)
    is_active_voice = not any(token.dep_ == "auxpass" for token in doc)

    if not (is_object_dependency and is_active_voice):
        return False

    for constituent in doc._.constituents:
        if constituent.label_ == "NP" and any(token.text in ACTOR_MARKERS for token in constituent):
            return True

    return False

def find_constituents_by_label(sent: Span, label: str) -> list[Span]:
    results = []
    for constituents in sent._.constituents:
        if label in constituents._.labels:
            results.append(constituents)
    return results

def determine_actor_vh(sentence: Span) -> Span | None:
    'Condition 1: subject dependency and NP < (actormarker)'
    for possible_actor in check_for_label_dominating_actor_marker(sentence, "NP"):
        if any(token.dep_ in subject_dependencies for token in possible_actor):
            return possible_actor

    print("Condition 2: object dependency and passive voice and PP < IN$(NP < (actormarker))")
    'Condition 2: object dependency and passive voice and PP < IN$(NP < (actormarker))'
    for possible_actor in check_for_label_dominating_actor_marker(sentence, "NP"):
        print("possible_actor:", possible_actor)
        is_object_dependency = any(token.dep_ in object_dependencies for token in possible_actor)
        print("is_object_dependency:", is_object_dependency)
        is_passive_voice = any(token.dep_ == "auxpass" for token in sent)
        print("is_passive_voice:", is_passive_voice)
        if not (is_object_dependency and is_passive_voice):
            print("not (is_object_dependency and is_passive_voice)")
            return None
        else:
            print("(is_object_dependency and is_passive_voice)")
            print("find_constituents_by_label", find_constituents_by_label(sentence, "PP"))
            print("possible_actor:", possible_actor)
            for possible_PP in find_constituents_by_label(sentence, "PP"):
                print("possible_PP:", possible_PP)
                for token in possible_PP:
                    print("child.text:", token.text, token.dep_, token.pos_, token.tag_)
                    if token.text == 'by' and 'IN' == token.tag_:
                        span_by = doc[token.i:token.i+1]
                        print(span_by)
                        print(immediately_dominates(possible_PP, span_by))
                        print(are_sisters(span_by, possible_actor))
                        print("Success!")
                #if are_sisters(possible_PP, possible_actor):
                 #   for child in possible_PP._.children:
                  #      print("child.text:", child.text, "child.dep_:", child.dep_)
                   #     if child.text == "by":
                    #        return possible_actor

    print("Condition 3: object dependency and active voice and NP < (actormarker))")
    'Condition 3: object dependency and active voice and NP < (actormarker))'
    for possible_actor in check_for_label_dominating_actor_marker(sentence, "NP"):
        is_object_dependency = any(token.dep_ in object_dependencies for token in possible_actor)
        is_active_voice = not any(token.dep_ == "auxpass" for token in sent)
        if not (is_object_dependency and is_active_voice):
            return None
        else:
            return possible_actor


"""
for const in sent._.constituents:
    if len(const._.labels) > 0 and const._.labels[0] == 'NP':
        print(const.text)"""

"""
 for token in sentence:
    print("token.sent._.labels:", token.sent._.labels)
    if token.dep_ in subject_dependencies and "NP" in token.sent._.labels:
        return token.text
    elif token.dep_ in object_dependencies and sentence_is_active == False and "PP" in token.sent._.labels:
        return token.text
    elif token.dep_ in object_dependencies and sentence_is_active == True and "NP" in token.sent._.labels:
        return token.text
"""

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('benepar', config={'model': 'benepar_en3'})


@Language.component("custom_sentencizer")  # TODO: me
def custom_sentencizer(doc):
    """Custom sentencizer that sets 'LS' tokens as sentence starts."""
    for token in doc:
        # By default, don't set anything (i.e., keep existing sent starts)
        # token.is_sent_start = False
        if token.tag_ == "LS":
            token.is_sent_start = True
    return doc

    # Register the custom sentencizer and add it to the pipeline before the parser


nlp.add_pipe("custom_sentencizer", before="parser")  # TODO: me
doc = nlp("""The organization shall determine:
a) what needs to be monitored and measured, including information security processes and controls;
b) the methods for monitoring, measurement, analysis and evaluation, as applicable, to ensure valid results. The methods selected should produce comparable and reproducible results to be considered valid;
c) when the monitoring and measuring shall be performed;
d) who shall monitor and measure;
e) when the results from monitoring and measurement shall be analysed and evaluated; and
f) who shall analyse and evaluate these results.
Documented information shall be available as evidence of the results. The organization shall evaluate the information security performance and the effectiveness of the information security management system.""")
doc = nlp("The dog was punished by the organization.")
# determine_actor_vh(list(doc.sents)[0])
# for sent in doc.sents:
sent = list(doc.sents)[0]
print(sent.text)
constituents = list(doc.sents)[0]._.parse_string
print(constituents)

for const in sent._.constituents:
    #print("const:", const)
    if len(const._.labels) > -1:
       print("const:", const, "*" * 20, "const._.labels", const._.labels)
# print("sent._.constituents", list(sent._.constituents))
print("sent._.labels", sent._.labels)
print("determine_actor_vh: ", determine_actor_vh(sent).__str__())
# determine_actor_vh(sent)


# labels = sentence._.labels

"""sent = list(doc.sents)[0]
constituents = list(sent._.constituents)
for const in constituents:
    # if len(const._.labels) > 0:
    print("const:", const, "*" * 20, "const._.labels", const._.labels)

A: Span = constituents[0]
print("A:", A.text)  # This is just an example, choose your own constituents.
B: Span = constituents[3]
print("B:", B.text)
print(dominates(A, B).__str__())"""
#

# determine_actor_vh(sent, True)
# print(are_sisters(sent._.constituents[0], sent._.constituents[1]).__str__())
# for const in sent._.constituents:
#   if len(const._.labels) > 0:
#      print("const:", const, "*" * 20, "const._.labels", const._.labels)


# if len(const._.labels)> 0 and const._.labels[0] == 'VP':
#   print(const.text)

# sent = list(doc.sents)[0]
# print(sent._.parse_string)
# (S (NP (NP (DT The) (NN time)) (PP (IN for) (NP (NN action)))) (VP (VBZ is) (ADVP (RB now))) (. .))
# print(sent._.labels)
# ('S',)
# print(list(sent._.children)[0])

# print(determine_actor_vh(sent, True))
