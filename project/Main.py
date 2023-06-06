import spacy
import warnings
import os
import coreferee
import benepar
import stanza
import spacy_stanza
from spacy import displacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

from AnalyzeSentence import analyze_document
from AnalyzeText import determine_marker, correct_order, construct
from Structure.Block import ConditionBlock
from Utilities import find_dependency


def download_all_dependencies():
    import nltk
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # benepar.download('benepar_en3')
    # benepar.download('benepar_en3_large')
    # nltk.download('wordnet')


if __name__ == '__main__':
    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
    warnings.filterwarnings('ignore')
    # download_all_dependencies()

    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_trf')
    # nlp = spacy_stanza.load_pipeline("en", download_method=None)

    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    nlp.add_pipe("spacy_wordnet", after='tagger')
    # nlp.add_pipe("spacy_wordnet")

    nlp.add_pipe('coreferee')

    text_input = open('Text/text05.txt', 'r').read().replace('\n', ' ')
    # text_input = "The first activity is to check and repair the hardware, whereas the second activity checks and configures the software."

    document = nlp(text_input)
    document._.coref_chains.print()
    print()

    # for sent in document.sents:
    #     print(sent._.parse_string)
    # displacy.serve(document, style="dep", port=5001)

    containerList = analyze_document(nlp, document)
    for container in containerList:
        determine_marker(container, nlp)
    correct_order(containerList)

    linked_list = construct(containerList)
    print(linked_list)
