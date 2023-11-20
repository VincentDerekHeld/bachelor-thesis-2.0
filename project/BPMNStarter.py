import spacy
import warnings
import os
import benepar
from spacy import Language

from project.AnalyzeSentence import analyze_document
from project.AnalyzeText import determine_marker, correct_order, build_flows, remove_redundant_processes, \
    determine_end_activities, adjust_actor_list
from project.BPMNCreator import create_bpmn_model_vh
from project.Constant import DEBUG
from project.Utilities import text_pre_processing, remove_introduction_sentence


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
    # Activate the following line to download all dependencies for the first time
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
        """Custom Sentencizer that sets 'LS' tokens as sentence starts. It is added to the pipeline before the parser.
           Here, it is not added, because the LLM resolves the problem with a higher quality."""
        for token in doc:
            if token.tag_ == "LS":
                token.is_sent_start = True
        return doc

    # Register the custom sentencizer and add it to the pipeline before the parser
    # nlp.add_pipe("custom_sentencizer", before="parser")

    try:
        text_input = open(input_path, 'r').read().replace('\n', ' ')
    except FileNotFoundError:
        print("Wrong file or file path to dir.")

    # text_input = preprocess_text_with_LLM(text_input) #TODO: Add this line to code
    text_input = text_pre_processing(text_input)

    # Example sentences could be filtered here, based on a rule based-approach, but the LLM resolves the problem with a higher quality.
    # text_input = filter_including_sentences(text_input)

    document = nlp(text_input)

    # Introduction sentences could be filtered here, based on a rule based-approach, but the LLM resolves the problem with a higher quality.
    # document = remove_introduction_sentence(document, nlp_similarity, nlp)
    if DEBUG: print("Document: " + document.text + "\n")

    containerList = analyze_document(document)
    for container in containerList:
        determine_marker(container, nlp)
    correct_order(containerList)
    remove_redundant_processes(containerList)

    from Playgrounds.Playgorund_Coreference import get_valid_actors_vh1
    valid_actors = get_valid_actors_vh1(containerList, nlp_similarity)  # TODO Check what was changed here
    # valid_actors = get_valid_actors(containerList)
    valid_actors = adjust_actor_list(valid_actors)
    flows = build_flows(containerList)
    for flow in flows:  # TODO: delte?
        print(flow)
    if DEBUG: print("Valid Actors: " + valid_actors.__str__() + "\n")
    determine_end_activities(flows)  # TODO
    # create_bpmn_model(flows, valid_actors, title, output_path)
    create_bpmn_model_vh(flows, valid_actors, title, output_path)
