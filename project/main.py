import spacy
import warnings
import os
import pyinflect
import benepar
import stanza
import spacy_stanza
from spacy import displacy


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


if __name__ == '__main__':
    os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
    warnings.filterwarnings('ignore')
    # download_all_dependencies()
    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_trf')
    # nlp = spacy_stanza.load_pipeline("en")
    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

    text_input = "The surgeon positions the balloon in an area of blockage and inflates it. the customer is interested in the product. the customer buys the item "
    # text_input = open('text.txt','r').read().replace('\n', ' ')
    doc = nlp(text_input)

    for sent in doc.sents:
        print(sent._.parse_string)

    displacy.serve(doc, port=5001, style="dep")

    # for sent in doc.sents:
    #     print(sent._.labels)
    #     print(sent._.parse_string)
    #     for child in sent._.children:
    #         print(child._.labels, "->", child)
    #         print(child._.parse_string)
