import spacy

def custom_sentence_split(text):
  """Splits a text into sentences using spaCy's dependency parser.

  Args:
    text: A string representing the text to be split.

  Returns:
    A list of strings, where each string represents a sentence.
  """

  # Load the spaCy language model
  nlp = spacy.load("en_core_web_trf")

  # Process the text with spaCy
  doc = nlp(text)

  # Initialize sentence boundaries
  sentence_start = 0
  sentence_end = 0

  # List to store the extracted sentences
  sentences = []

  # Iterate over the tokens in the document
  for token in doc:
    # If the token is a sentence boundary, append the current sentence to the list
    if token.is_sent_start:
      sentences.append(doc[sentence_start:sentence_end].text.strip())

      # Update the sentence boundaries for the next iteration
      sentence_start = sentence_end

    sentence_end += 1

  # Append the last sentence if there is any remaining text
  if sentence_start < len(doc):
    sentences.append(doc[sentence_start:].text.strip())

  return sentences

# Input text without line breaks
input_text = """The organization shall determine: a) "what needs to be monitored and measured, including information security processes and controls;" b) the methods for monitoring, measurement, analysis and evaluation, as applicable, to ensure valid results. The methods selected should produce comparable and reproducible results to be considered valid; c) when the monitoring and measuring shall be performed; d) who shall monitor and measure; e) when the results from monitoring and measurement shall be analysed and evaluated; and f) who shall analyse and evaluate these results. Documented information shall be available as evidence of the results. The organization shall evaluate the information security performance and the effectiveness of the information security management system. """

# Split the text into sentences
sentences = custom_sentence_split(input_text)

# Print the extracted sentences
for i, sentence in enumerate(sentences, start=1):
  print(f"Sentence {i}: {sentence}")
