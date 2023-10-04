import spacy


def load_all_texts(texts=[]) -> list[str]:
    itaration = 1
    while itaration < 24:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis-shuiwei/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis-shuiwei/Evaluation/Text1" + itaration.__str__() + ".png"
        # BPMNStarter.start_task(input_path, "example", output_path)
        texts.append(open(input_path, 'r').read().replace('\n', ' '))
        itaration += 1
    return texts


texts = load_all_texts()


def check_for_introdutction_sentence(text, nlp):
    doc = nlp(text)
    return list(doc.sents)[0].similarity(doc)


nlp = spacy.load("en_core_web_lg")
"""
# Print each text with a label
for index, text in enumerate(texts, 1):
    similarity_score = check_for_introdutction_sentence(text, nlp)
    doc = nlp(text)
    print(f"Text {index}:  similarity_score: {similarity_score} --- {list(doc.sents)[0]}\n")
load_all_texts()
"""

