# Initialisieren Sie Variablen
formatted_sentences = []
current_prefix = ""

for token in doc:
    # Print the text and the predicted part-of-speech tag
    print("{:<14}{:<14}{:<14}{:<14}{:<14}{:<14}".format(token.text, token.pos_, token.tag_, token.dep_, token.orth_,
                                                        token.lemma_))

for i, formatted_sent in enumerate(list(doc.sents)):
    print(f"Sentence {i + 1}: {formatted_sent}")

# Geben Sie die umgewandelten Sätze aus
for i, formatted_sent in enumerate(formatted_sentences):
    print(f"Sentence {i + 1}: {formatted_sent}")
