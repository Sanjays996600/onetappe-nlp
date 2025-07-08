import spacy
from spacy.matcher import Matcher
import logging

# Setup logging for unmatched inputs
logging.basicConfig(filename='unmatched_inputs.log', level=logging.INFO)

# Load blank English model
nlp = spacy.blank('en')

# Define service types and pincodes patterns
service_types = ['electrician', 'plumber', 'carpenter', 'painter', 'cleaner']

matcher = Matcher(nlp.vocab)

# Add patterns for service types
for service in service_types:
    pattern = [{'LOWER': service}]
    matcher.add('SERVICE_TYPE', [pattern])

# Add pattern for area code / pincode (assuming 6 digit numbers)
pincode_pattern = [{'IS_DIGIT': True, 'LENGTH': 6}]
matcher.add('PINCODE', [pincode_pattern])

def extract_entities(text):
    doc = nlp(text.lower())
    matches = matcher(doc)
    entities = {'service_type': None, 'pincode': None}
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        if label == 'SERVICE_TYPE' and entities['service_type'] is None:
            entities['service_type'] = span.text
        elif label == 'PINCODE' and entities['pincode'] is None:
            entities['pincode'] = span.text
    # Log unmatched inputs
    if entities['service_type'] is None or entities['pincode'] is None:
        logging.info(f"Unmatched input: {text}")
    return entities

if __name__ == '__main__':
    test_text = "I need an electrician in 560001"
    print(extract_entities(test_text))