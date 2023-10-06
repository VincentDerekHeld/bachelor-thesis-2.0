import spacy
import benepar

# Load SpaCy model with benepar
nlp = spacy.load('en_core_web_lg')
benepar_integration = benepar.BeneparComponent("benepar_en3")
nlp.add_pipe(benepar_integration)

def is_PP_IN_by(token):
    if 'PP' in token._.labels:
        for child in token.children:
            if child.text == 'by' and 'IN' in child._.labels:
                return True
    return False

def is_sibling_of_PP_IN_by(span):
    parent = span.root.head
    for child in parent.children:
        if is_PP_IN_by(child):
            return True
    return False

doc = nlp("The task was completed by the engineer.")
span = doc[5:7]  # the engineer
print(span)
print(is_sibling_of_PP_IN_by(span))
