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
from AnalyzeText import determine_marker, correct_order
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

    # text_input = open('Text/text01.txt', 'r').read().replace('\n', ' ')
    text_input = "The first activity is to check and repair the hardware. The first step solved the problem. "

    document = nlp(text_input)
    document._.coref_chains.print()

    contain = analyze_document(nlp, document)
    for cont in contain:
        determine_marker(cont, nlp)
    correct_order(contain)
    for sent in contain:
        for proc in sent.processes:

            print("-" * 10)
            marker = proc.action.marker
            if marker is not None:
                print(marker + "->")

            actor = proc.actor
            action = proc.action
            obj = action.object

            if actor is not None:
                if len(actor.resolved_token) > 0:
                    print("Actor: ", end="")
                    print(actor.resolved_token)
                else:
                    print("Actor: " + actor.token.text)
            if action is not None:
                print("Action: " + action.token.text)
            if obj is not None:
                if len(obj.resolved_token) > 0:
                    print("Object: ", end="")
                    print(obj.resolved_token)
                else:
                    print("Object: " + obj.token.text)

            print("-" * 10)
