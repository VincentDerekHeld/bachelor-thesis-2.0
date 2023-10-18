import spacy
import warnings
import os
import coreferee
import benepar
from spacy import Language
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

from Playgrounds.Playground_Filtering import filter_including_sentences
from Playgrounds.Playground_Introduction_sentence import remove_introduction_sentence
from project.AnalyzeSentence import analyze_document, analyze_document_vh, analyze_document_vh1
from project.AnalyzeText import determine_marker, correct_order, build_flows, get_valid_actors, \
    remove_redundant_processes, determine_end_activities, adjust_actor_list
from project.BPMNCreator import create_bpmn_model, create_bpmn_model_vh
from Playgrounds.Playground_Actors_Similarity import get_valid_actors_vh
from project.Utilities import text_pre_processing


def download_all_dependencies():
    import nltk
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    benepar.download('benepar_en3')
    benepar.download('benepar_en3_large')
    nltk.download('wordnet')


def start_task(input_path, title, output_path, debug=False):
    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
    warnings.filterwarnings('ignore')
    # download_all_dependencies()

    nlp = spacy.load('en_core_web_trf')
    nlp_similarity = spacy.load("en_core_web_lg")

    if debug:
        benepar.download('benepar_en3')
        nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    else:
        benepar.download('benepar_en3_large')
        nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})

    nlp.add_pipe("spacy_wordnet", after='tagger')
    nlp.add_pipe('coreferee')

    @Language.component("custom_sentencizer")  # TODO: me
    def custom_sentencizer(doc):
        """Custom sentencizer that sets 'LS' tokens as sentence starts."""
        for token in doc:
            # By default, don't set anything (i.e., keep existing sent starts)
            # token.is_sent_start = False
            if token.tag_ == "LS":
                token.is_sent_start = True
        return doc

    # Register the custom sentencizer and add it to the pipeline before the parser
    nlp.add_pipe("custom_sentencizer", before="parser")  # TODO: me

    text_input = open(input_path, 'r').read().replace('\n', ' ')
    text_input = text_pre_processing(text_input)
    text_input = filter_including_sentences(text_input)  # TODO: me
    document = nlp(
        text_input)  # TODO: Text Input could be a paramter of remove_introduction_sentence, so we do not need
    document = remove_introduction_sentence(document, nlp_similarity, nlp)  # TODO: me
    print("Document: " + document.text + "\n")

    containerList = analyze_document_vh1(document)
    #containerList = analyze_document(document)
    for container in containerList:
        determine_marker(container, nlp)
    correct_order(containerList)
    remove_redundant_processes(containerList)

    from Playgrounds.Playgorund_Coreference import get_valid_actors_vh1
    valid_actors = get_valid_actors_vh1(containerList, nlp_similarity)
    #valid_actors = get_valid_actors(containerList)
    valid_actors = adjust_actor_list(valid_actors)
    flows = build_flows(containerList)
    for flow in flows:
        print(flow)
    print("Valid Actors: " + valid_actors.__str__() + "\n")
    determine_end_activities(flows)
    #create_bpmn_model(flows, valid_actors, title, output_path)
    create_bpmn_model_vh(flows, valid_actors, title, output_path)
