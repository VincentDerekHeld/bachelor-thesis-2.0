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
from AnalyzeText import determine_marker, correct_order, build_flows, get_valid_actors, build_linked_list, \
    remove_redundant_processes, determine_end_activities
from BPMNCreator import create_bpmn_model
from Utilities import text_pre_processing


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

    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    # nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    nlp.add_pipe("spacy_wordnet", after='tagger')
    # nlp.add_pipe("spacy_wordnet")

    nlp.add_pipe('coreferee')

    text_input = open('Text/text02.txt', 'r').read().replace('\n', ' ')
    # text_input = "Every time we get a new order from the sales department, first, one of my masters determines the necessary parts and quantities as well as the delivery date."

    text_input = text_pre_processing(text_input)
    document = nlp(text_input)

    document._.coref_chains.print()
    print()

    containerList = analyze_document(document)
    for container in containerList:
        determine_marker(container, nlp)
    correct_order(containerList)
    # remove_redundant_processes(containerList)
    flows = build_flows(containerList)
    determine_end_activities(flows)


    valid_actors = get_valid_actors(containerList)
    create_bpmn_model(flows, valid_actors, "debug02", "/Users/shuaiwei_yu/Downloads/text02_test.png")

    print(build_linked_list(containerList))
