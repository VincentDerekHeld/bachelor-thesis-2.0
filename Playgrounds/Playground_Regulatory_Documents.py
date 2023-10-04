import spacy
from spacy import Language
from spacy.tokens import Span, Token

from project.Utilities import text_pre_processing

nlp = spacy.load("en_core_web_trf")

# Der gegebene Text
text5 = """The organization shall determine:
    a) what needs to be monitored and measured, including information security processes and controls;
    b) the methods for monitoring, measurement, analysis and evaluation, as applicable, to ensure valid results. The methods selected should produce comparable and reproducible results to be considered valid;
    c) when the monitoring and measuring shall be performed;
    d) who shall monitor and measure;
    e) when the results from monitoring and measurement shall be analysed and evaluated; and
    f) who shall analyse and evaluate these results.
Documented information shall be available as evidence of the results. The organization shall evaluate the information security performance and the effectiveness of the information security management system."""

text6 = """The organization shall plan, establish, implement and maintain an audit programme(s), including the frequency, methods, responsibilities, planning requirements and reporting. 
When establishing the internal audit programme(s), the organization shall consider the importance of the processes concerned and the results of previous audits.
The organization shall: 
    a) define the audit criteria and scope for each audit;
    b) select auditors and conduct audits that ensure objectivity and the impartiality of the audit process;
    c) ensure that the results of the audits are reported to relevant management; 
Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results."""

text7 = """Top management shall review the organization's information security management system at planned intervals to ensure its continuing suitability, adequacy and effectiveness.
The management review shall include consideration of:
    a) the status of actions from previous management reviews;
    b) changes in external and internal issues that are relevant to the information security management system;
    c) changes in needs and expectations of interested parties that are relevant to the information security management system;
    d) feedback on the information security performance, including trends in:
        1) nonconformities and corrective actions;
        2) monitoring and measurement results;
        3) audit results; 
        4) fulfilment of information security objectives;
    e) feedback from interested parties;
    f) results of risk assessment and status of risk treatment plan; 
    g) opportunities for continual improvement.
The results of the management review shall include decisions related to continual improvement opportunities and any needs for changes to the information security management system.
Documented information shall be available as evidence of the results of management reviews.
"""

text8 = """In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.

The processor shall notify the controller without undue delay after becoming aware of a personal data breach.

The notification referred to in paragraph 1 shall at least describe the nature of the personal data breach including where possible, the categories and approximate number of data subjects concerned and the categories and approximate number of personal data records concerned.

The notification referred to in paragraph 1 shall at least communicate the name and contact details of the data protection officer or other contact point where more information can be obtained.

The notification referred to in paragraph 1 shall at least describe the likely consequences of the personal data breach.

The notification referred to in paragraph 1 shall at least describe the measures taken or proposed to be taken by the controller to address the personal data breach, including, where appropriate, measures to mitigate its possible adverse effects.

Where, and in so far as, it is not possible to provide the information at the same time, the information may be provided in phases without undue further delay.

The controller shall document any personal data breaches, comprising the facts relating to the personal data breach, its effects and the remedial action taken. That documentation shall enable the supervisory authority to verify compliance with this Article.
"""


def contains_colon_and_ls(doc):
    """
    Checks if the doc contains a ":" and then, at some position after the ":",
    contains a token where token.POS_ == "LS".
    """
    has_colon = False
    for token in doc:
        if token.text == ":":
            has_colon = True
        if has_colon and token.tag_ == "LS":
            return True
    return False


def get_span_before_colon(doc):
    """
    Returns the span before the first ":" in the doc.
    """
    colon_pos = [token.i for token in doc if token.text == ":"][0]
    return doc[0:colon_pos]


def extract_text_between_ls_and_punct(doc):
    """
    Extracts text between a token with token.tag_ == "LS" and the next ".", "!" or "?".
    Returns a list of such extracted texts if multiple are found.
    """
    recording = False
    results = []
    current_text = []

    for token in doc:
        if token.tag_ == "LS":
            recording = True
            current_text = [token.text]
        elif recording and token.text in [";"]:
            recording = False
            results.append(" ".join(current_text))
            current_text = []
        elif recording:
            current_text.append(token.text)

    return results


def find_ls_indexes(doc):
    """Find all token indexes where token.tag_ == 'LS'."""
    return [token.i for token in doc if token.tag_ == "LS"]


def split_text_on_indexes(doc, indexes):
    """Split the doc text before each index."""
    text_splits = []
    start = 0
    for idx in indexes:
        # Convert token index to char index
        char_idx = doc[idx].idx
        text_splits.append(doc.text[start:char_idx])
        start = char_idx
    # Add the remaining text after the last index
    text_splits.append(doc.text[start:])
    return text_splits


@Language.component("custom_sentencizer")
def custom_sentencizer(doc):
    """Custom sentencizer that sets 'LS' tokens as sentence starts."""
    indexes = find_ls_indexes(doc)
    for token in doc:
        # By default, don't set anything (i.e., keep existing sent starts)
        # token.is_sent_start = False
        if token.tag_ == "LS":
            token.is_sent_start = True
    return doc


input_path = "//project/Text/text_input_vh/Text5.txt"
text_input = open(input_path, 'r').read().replace('\n',
                                                  ' ')
pre_processed_text = text_pre_processing(text_input)

# Register the custom sentencizer and add it to the pipeline before the parser
nlp.add_pipe("custom_sentencizer", before="parser")

doc = nlp(pre_processed_text)

# doc = set_ls_as_sent_starts(doc)

# Print sentences to verify

#for i, sent in enumerate(doc.sents):
 #   print(f"Sententence {i}: {sent.text} \n")

import re

s = pre_processed_text

stop_items = [".", "!", ";"]
pattern = r', including[^' + ''.join(stop_items) + ']*?(?=[' + ''.join(stop_items) + '])'
filtered_string = re.sub(pattern, '', s)


print(filtered_string)


# indexes = find_ls_indexes(doc)
# splits = split_text_on_indexes(doc, indexes)
# print(splits)

# results = extract_text_between_ls_and_punct(doc)

# line_break_positions = [token.i for token in doc if token.text == "\n"]

# print(line_break_positions)
# for res in results:
#   print(res)
# print(contains_colon_and_ls(doc))
"""
for token in doc:
    if token.text == ":":
        token_index = token.i
"""
