import spacy

nlp = spacy.load("en_core_web_trf")

text = "Documented information shall be available as evidence of the results of management reviews."
text1 = "The boy is running."

doc = nlp(text)
for token in doc:
    print(token.text, token.pos_, token.dep_, token.lemma_, token.head.text)