import spacy
import coreferee
import benepar
from spacy import displacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

from Utilities import text_pre_processing

if __name__ == '__main__':
    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_trf')

    # nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    # nlp.add_pipe('coreferee')

    # text_input = open('Text/text_input/text16.txt', 'r').read().replace('\n', ' ')
    text_input = "CRS checks the defect and hands out a repair cost calculation back"

    # text_input = text_pre_processing(text_input)
    document = nlp(text_input)

    # print(spacy.explain("PART"))

    # for sent in document.sents:
    #     print(sent._.parse_string)
    #     print()
    displacy.serve(document, style="dep", port=5001)
