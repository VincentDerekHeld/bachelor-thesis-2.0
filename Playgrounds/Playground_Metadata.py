import spacy


def similarity_sentence_to_full_text(input: str, text_number):
    print("Text: " + text_number.__str__() + "\n")
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(input)
    for i, sent in enumerate(doc.sents):
        print("\t Similarity: " + round(sent.similarity(doc),
                                        2).__str__() + " for sentence no." + i.__str__() + ":  " + sent.text + "\n")


def check_texts_stopwords(input: str, text_number):
    print("Text: " + text_number.__str__() + "\n")
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(input)
    for i, sent in enumerate(doc.sents):
        for token in sent:
            if token.is_stop:
                print("{:<14}{:<14}{:<14}{:<14}{:<14}".format(token.text, token.pos_, token.tag_, token.dep_,
                                                              token.is_stop))
        print("\n")


def check_ents(input: str, text_number):
    print("Text: " + text_number.__str__() + "\n")
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(input)
    for i, sent in enumerate(doc.sents):
        print("Sentence: " + sent.text + "\n")
        for ent in sent.ents:
            print("\t", ent.text, ent.label_)
        print("\n")


def print_all_texts(input: str, text_number):
    print("Text: " + text_number.__str__() + "\n"
          + input + "\n")

def remove_introduction_sentence(doc: spacy.tokens.doc.Doc, nlp_similarity, nlp) -> spacy.tokens.doc.Doc:
    doc_new = nlp_similarity(doc.text)
    sentences = list(doc_new.sents)
    # Check similarity between the first sentence and the entire document
    print("Similarity: " + sentences[0].similarity(doc_new).__str__() + " for sentence: " + sentences[0].text)
    if sentences[0].similarity(doc_new) < 0.8:
        print("First sentence is an introduction sentence")
        # If the condition is met, reconstruct the document without the first sentence
        new_text = ' '.join([sent.text for sent in sentences[1:]])
        doc = nlp(new_text)
    return doc


def run__all_texts():
    itaration = 1
    while itaration <= 23:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        text_input = open(input_path, 'r').read().replace('\n', ' ')
        check_ents(text_input, itaration)
        itaration += 1


run__all_texts()
