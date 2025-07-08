# Multilingual NLP Integration Guide

This guide provides detailed instructions for integrating the enhanced multilingual NLP system with the existing WhatsApp chatbot backend.

## Overview

The integration process involves replacing the current NLP processing pipeline with the new multilingual system that supports English, Hindi, and mixed language inputs. The new system provides improved accuracy, better language detection, and enhanced entity extraction.

## Integration Steps

### 1. Update Dependencies

Ensure all required dependencies are installed:

```bash
pip install -r requirements.txt
```

Download the required spaCy models:

```bash
python -m spacy download en_core_web_md
python -m spacy download xx_ent_wiki_sm
```

### 2. File Structure Updates

Add the following new files to your project:

- `enhanced_language_model.py` - Core multilingual NLP implementation
- `chatbot_integration.py` - Integration with WhatsApp chatbot
- `training_data_generator.py` - (Optional) For generating training data
- `model_evaluation.py` - (Optional) For evaluating model performance

### 3. Code Integration

#### Option 1: Direct Replacement

Replace the existing NLP processing in your WhatsApp handler with the new `ChatbotIntegration` class:

```python
# In your WhatsApp message handler
from chatbot_integration import ChatbotIntegration

# Initialize the chatbot integration
chatbot = ChatbotIntegration()

def handle_whatsapp_message(message, user_id):
    # Process the message using the new multilingual system
    response = chatbot.process_message(message, user_id)
    
    # Send the response back to WhatsApp
    send_whatsapp_response(user_id, response)
```

#### Option 2: Gradual Integration

If you prefer a more gradual approach, you can integrate only the enhanced language detection first:

```python
from enhanced_language_model import detect_language_with_confidence, detect_mixed_language

def handle_whatsapp_message(message, user_id):
    # Use enhanced language detection
    language, confidence = detect_language_with_confidence(message)
    is_mixed = detect_mixed_language(message)
    
    if is_mixed:
        # Handle mixed language input
        # ...
    elif language == "en":
        # Use existing English processing
        # ...
    elif language == "hi":
        # Use existing Hindi processing
        # ...
    else:
        # Handle unsupported language
        # ...
```

### 4. API Integration

Update the API endpoint mappings in `chatbot_integration.py` to match your actual backend API endpoints:

```python
API_ENDPOINTS = {
    "get_inventory": "/seller/inventory",
    "get_low_stock": "/seller/inventory/low-stock",
    "get_report": "/seller/reports",
    "get_top_products": "/seller/reports/top-products",
    "get_customer_data": "/seller/customers/analytics",
    "add_product": "/seller/products/add",
    "edit_stock": "/seller/products/update-stock",
    "get_orders": "/seller/orders",
    "search_product": "/seller/products/search"
}
```

### 5. Response Template Customization

Customize the response templates in `chatbot_integration.py` to match your business requirements:

```python
ENGLISH_RESPONSE_TEMPLATES = {
    "get_inventory": "Here's your current inventory:\n{inventory_list}",
    "get_low_stock": "Products with low stock:\n{low_stock_list}",
    # Add more templates as needed
}

HINDI_RESPONSE_TEMPLATES = {
    "get_inventory": "आपका वर्तमान इन्वेंटरी:\n{inventory_list}",
    "get_low_stock": "कम स्टॉक वाले प्रोडक्ट्स:\n{low_stock_list}",
    # Add more templates as needed
}
```

### 6. Testing the Integration

Test the integration with various inputs to ensure it works correctly:

```python
from chatbot_integration import ChatbotIntegration

chatbot = ChatbotIntegration()

# Test English commands
english_tests = [
    "Show my inventory",
    "Update rice stock to 50",
    "Get orders from last week",
    "Show low stock items",
    "Search for rice products"
]

# Test Hindi commands
hindi_tests = [
    "मेरा इन्वेंटरी दिखाओ",
    "चावल का स्टॉक 50 करो",
    "पिछले हफ्ते के ऑर्डर दिखाओ",
    "कम स्टॉक वाले आइटम दिखाओ",
    "चावल प्रोडक्ट्स खोजो"
]

# Test mixed language commands
mixed_tests = [
    "Show मेरा inventory",
    "Update चावल stock to 50",
    "Get orders पिछले हफ्ते से",
    "Show कम stock items",
    "Search for चावल products"
]

# Run tests
for test in english_tests + hindi_tests + mixed_tests:
    print(f"Input: {test}")
    response = chatbot.process_message(test, "test_user")
    print(f"Response: {response}\n")
```

## Advanced Configuration

### Adjusting Language Detection Thresholds

You can adjust the language detection thresholds in `enhanced_language_model.py`:

```python
def detect_language_with_confidence(text, threshold=0.6):
    # Adjust threshold as needed
    # ...

def detect_mixed_language(text, threshold=0.3):
    # Adjust threshold as needed
    # ...
```

### Enabling ML-based Intent Recognition

To enable the transformer-based intent recognition:

1. Generate training data:

```bash
python training_data_generator.py
```

2. Train the model:

```python
from enhanced_language_model import train_intent_classifier

train_intent_classifier("./data/training_data.json", "./models/intent_classifier")
```

3. Update the `recognize_intent` function to use the ML model:

```python
def recognize_intent(text, language, use_ml_model=True):
    # Set use_ml_model to True
    # ...
```

## Monitoring and Maintenance

### Logging

Implement logging to monitor the NLP system's performance:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nlp_system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("multilingual_nlp")

# In ChatbotIntegration class
def process_message(self, message, user_id):
    logger.info(f"Processing message: {message} for user: {user_id}")
    # ...
```

### Regular Evaluation

Regularly evaluate the system's performance using the evaluation script:

```bash
python model_evaluation.py
```

Review the evaluation results to identify areas for improvement.

### Continuous Improvement

1. Collect misclassified inputs and add them to the training data
2. Update regex patterns for frequently misclassified intents
3. Add new entity extraction rules for new product types or categories
4. Retrain the ML model periodically with new data

## Troubleshooting

### Common Issues and Solutions

1. **Incorrect Language Detection**
   - Adjust language detection thresholds
   - Add more character frequency analysis for specific languages

2. **Intent Recognition Failures**
   - Add more regex patterns for the problematic intent
   - Add more training examples for the ML model

3. **Entity Extraction Issues**
   - Update regex patterns for entity extraction
   - Add more specific rules for problematic entity types

4. **API Integration Errors**
   - Verify API endpoint URLs
   - Check parameter formatting
   - Implement better error handling

### Debugging

Enable debug logging for more detailed information:

```python
logging.basicConfig(level=logging.DEBUG)
```

Add debug points in key functions:

```python
def parse_multilingual_command(text):
    logger.debug(f"Parsing command: {text}")
    language, confidence = detect_language_with_confidence(text)
    logger.debug(f"Detected language: {language} with confidence: {confidence}")
    # ...
```

## Performance Optimization

### Caching

Implement caching for frequently used patterns and responses:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def detect_language_with_confidence(text, threshold=0.6):
    # Implementation
    # ...
```

### Lazy Loading

Implement lazy loading for the transformer model:

```python
class TransformerIntentClassifier:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TransformerIntentClassifier()
        return cls._instance
```

## Conclusion

By following this integration guide, you should be able to successfully integrate the enhanced multilingual NLP system with your existing WhatsApp chatbot. The new system provides improved accuracy, better language detection, and enhanced entity extraction for both English and Hindi languages, as well as mixed language inputs.

For any issues or questions, please refer to the troubleshooting section or contact the development team.