import spacy

# Laden Sie das spaCy-Modell
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
# Verarbeiten Sie den Text mit spaCy
doc = nlp(text7)

# Initialisieren Sie Variablen
formatted_sentences = []
current_prefix = ""

for token in doc:
    # Print the text and the predicted part-of-speech tag
    print("{:<14}{:<14}{:<14}{:<14}{:<14}{:<14}".format(token.text, token.pos_, token.tag_, token.dep_, token.orth_,
                                                        token.lemma_))



for i, formatted_sent in enumerate(list(doc.sents)):
    print(f"Sentence {i + 1}: {formatted_sent}")

# Geben Sie die umgewandelten Sätze aus
for i, formatted_sent in enumerate(formatted_sentences):
    print(f"Sentence {i + 1}: {formatted_sent}")

