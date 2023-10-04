"""
Change the way how sentences are splitted and make every list item to an own sentence

"""

import spacy

from project.Utilities import text_pre_processing

input_path = "//project/Text/text_input_vh/Text05.txt"

text_input = text_pre_processing(open(input_path, 'r').read().replace('\n', ' '))

nlp = spacy.load('en_core_web_trf')

print("Token Attributes: \n", "token.text, token.pos_, token.tag_, token.dep_, token.orth_")


@spacy.Language.component("custom_sentence_boundary")
def custom_sentence_boundary(doc):
    for token in doc:
        if token.tag_ == "LS":
            token.sent_start = True
    return doc


# Add the custom component to the pipeline using its name
nlp.add_pipe("custom_sentence_boundary", before="parser")

doc1 = nlp(text_input)

for token in doc1:
    # Print the text and the predicted part-of-speech tag
    print("{:<14}{:<14}{:<14}{:<14}{:<14}{:<14}".format(token.text, token.pos_, token.tag_, token.dep_, token.orth_,
                                                        token.lemma_))

# print(f"Token '{token.text}' is the start of a sentence.")

for sent in doc1.sents:
    print(sent.text, "\n \n")