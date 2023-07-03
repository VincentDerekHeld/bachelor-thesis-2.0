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
    remove_redundant_processes, determine_end_activities, adjust_actors
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

    # text_input = open('Text/text10.txt', 'r').read().replace('\n', ' ')
    text_input = "Whenever the sales department receives an order, a new process instance is created.This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. A member of the sales department can then reject or accept the order for a customized bike."

    text_input = text_pre_processing(text_input)
    document = nlp(text_input)

    document._.coref_chains.print()
    print()

    containerList = analyze_document(document)
    for container in containerList:
        determine_marker(container, nlp)
    correct_order(containerList)
    remove_redundant_processes(containerList)

    valid_actors = get_valid_actors(containerList)
    # adjust_actors(containerList, valid_actors)
    flows = build_flows(containerList)
    determine_end_activities(flows)

    create_bpmn_model(flows, valid_actors, "debug", "/Users/shuaiwei_yu/Desktop/output/text10_test.png")

    # print(build_linked_list(containerList))
