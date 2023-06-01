import spacy
import coreferee
import benepar
from spacy import displacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

from AnalyzeSentence import analyze_document
from AnalyzeText import determine_marker, correct_order, construct
from Structure.Block import ConditionBlock
from Utilities import find_dependency

if __name__ == '__main__':
    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_trf')

    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    nlp.add_pipe('coreferee')

    text_input = open('Text/text01.txt', 'r').read().replace('\n', ' ')
    #
    # text_input = "A customer brings in a defective computer and the CRS checks the defect and hands out a repair cost calculation back."

    document = nlp(text_input)

    for sent in document.sents:
        print(sent._.parse_string)
    displacy.serve(document, style="dep", port=5001)
