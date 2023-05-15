import spacy
import warnings
import os
import coreferee
import benepar
import stanza
import spacy_stanza
from spacy import displacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

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

    # nlp.add_pipe("spacy_wordnet", after='tagger')
    # nlp.add_pipe("spacy_wordnet")

    nlp.add_pipe('coreferee')

    # text_input = "In case of customer accepting the offer, the salesperson will base on this close the deal. " \
    #              "Otherwise, the salesperson will offer a lower price. " \
    #              "In the meantime, the customer prepares the payment. " \
    #              "subsequently the salesperson delivers the product."
    text_input = "Based on the result we go there. Based on this, we leave. Based of that, we move."

    # text_input = open('Text/text01.txt', 'r').read().replace('\n', ' ')

    doc = nlp(text_input)

    # doc._.coref_chains.print()

    for sent in doc.sents:
        print(sent._.parse_string)
        # print(find_dependency(["xcomp"], sentence=sent))
        for token in sent:
            print(token.text, token.pos_, token.tag_, token.dep_)


    displacy.serve(doc, port=5001, style="dep")