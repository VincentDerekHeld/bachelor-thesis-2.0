import spacy

nlp = spacy.load("en_core_web_trf")
itaration = 1
while itaration <= 23:
    input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text1.txt"
    text_input = open(input_path, 'r').read().replace('\n', ' ')
    doc = nlp(text_input)
    #print(doc.text)
    print("Text" + itaration.__str__()+":")
    for ent in doc.ents:
        print(ent.text, ent.label_)
    itaration += 1
