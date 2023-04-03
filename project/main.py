import spacy
from spacy.tokens import Span
from spacy.matcher import Matcher
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

# read file from text.txt and load it into text_input and ignore \n
with open('text.txt', 'r') as f:
    text_input = f.read().replace('\n', '')

doc = nlp(text_input)

# displacy.serve(doc, port=5001, style="dep")

# for sent in doc.sents:
#     print(sent.root)
#
#     for child in sent.root.children:
#         if child.dep_ == 'nsubj':
#             span = Span(doc, child.i, child.i + 1, label="Who")
#             doc.ents = list(doc.ents) + [span]
#
#     for child in sent.root.conjuncts:
#         for subchild in child.children:
#             if subchild.dep_ == 'nsubj':
#                 span = Span(doc, child.i, child.i + 1, label="Who")
#                 doc.ents = list(doc.ents) + [span]

# displacy.serve(doc, port=5001, style="dep")

matcher = Matcher(nlp.vocab)

pattern_1 = [
    {"POS": {"IN": ["PROPN", "NOUN"]}},
    {"POS": "VERB"},
    {"POS": "ADP", "OP": "?"},
    {"POS": "DET", "OP": "?"},
    {"POS": "ADJ", "OP": "*"},
    {"POS": "NOUN", "OP": "+"}
]




matcher.add("PATTERN_1", [pattern_1])

matches = matcher(doc)
for match_id, start, end in matches:
    # Get the matched span
    matched_span = doc[start:end]
    print(matched_span.text)

# write a match pattern that checks for a verb followed by a noun


