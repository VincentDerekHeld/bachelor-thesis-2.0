import spacy


def number_of_sentences():
    itaration = 1
    while itaration < 24:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        text_input = open(input_path, 'r').read().replace('\n', ' ')
        nlp = spacy.load('en_core_web_trf')
        doc = nlp(text_input)
        number_of_sentences = len(list(doc.sents))
        print(f"Text{itaration.__str__()}: {number_of_sentences}")
        itaration += 1


def number_of_tokens():
    itaration = 1
    while itaration < 24:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        text_input = open(input_path, 'r').read().replace('\n', ' ')
        nlp = spacy.load('en_core_web_trf')
        doc = nlp(text_input)
        number_of_tokens = len(list(doc))
        print(f"Text{itaration.__str__()}: {number_of_tokens}")
        itaration += 1

number_of_tokens()