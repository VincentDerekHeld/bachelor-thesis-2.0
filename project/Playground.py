import spacy
import coreferee
import benepar
from spacy import displacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

from Utilities import text_pre_processing

if __name__ == '__main__':
    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_trf')

    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    nlp.add_pipe('coreferee')

    # text_input = open('Text/text09.txt', 'r').read().replace('\n', ' ')
    text_input = "The first activity is to check and repair the hardware. The Evanstonian is an upscale independent hotel. The waiter is also responsible for nonalcoholic drinks. If the customer is high risk, the loan is denied."

    text_input = text_pre_processing(text_input)
    document = nlp(text_input)

    for sent in document.sents:
        print(sent._.parse_string)
        print()
    displacy.serve(document, style="dep", port=5001)
