"""
Check, wheater the first sentence is a introduction sentence (-> irrelevant for the process diagram) for the text or not.
"""
import spacy

from Playgrounds.Playground_Load_All_Texts import load_all_texts


def remove_introduction_sentence(doc: spacy.tokens.doc.Doc, nlp_similarity, nlp) -> spacy.tokens.doc.Doc:
    doc_new = nlp_similarity(doc.text)
    sentences = list(doc_new.sents)
    # Check similarity between the first sentence and the entire document
    print("Similarity: " + sentences[0].similarity(doc_new).__str__() + " for sentence: " + sentences[0].text)
    if sentences[0].similarity(doc_new) < 0.9:
        print("First sentence is an introduction sentence")
        # If the condition is met, reconstruct the document without the first sentence
        new_text = ' '.join([sent.text for sent in sentences[1:]])
        doc = nlp(new_text)
    return doc
