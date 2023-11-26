import spacy

# Load a spaCy model
nlp = spacy.load('en_core_web_trf')

# Your text
text = "This is a sample text for processing with spaCy."

# Process the text
doc = nlp(text)

# Filter tokens
filtered_tokens = []
for token in doc:
    # Remove stop words and punctuation, and apply any other custom filters

    #if not token.is_stop and not token.is_punct and len(token.text) > 2:
    if not token.is_stop:
        filtered_tokens.append(token.text)

# Print the filtered tokens
print(filtered_tokens)