# Multilingual NLP Chatbot Implementation

## Overview

This project implements a comprehensive multilingual Natural Language Processing (NLP) system for a WhatsApp chatbot, supporting both English and Hindi languages with mixed language detection capabilities. The system processes user commands, extracts intents and entities, and generates appropriate responses.

## Key Features

- **Multilingual Support**: Full support for English and Hindi languages
- **Mixed Language Detection**: Ability to identify and process messages containing both languages
- **Enhanced Intent Recognition**: Hybrid approach using both rule-based patterns and ML models
- **Advanced Entity Extraction**: Extract product names, quantities, dates, and other entities
- **Confidence Scoring**: Provides confidence levels for language and intent detection
- **Transformer Integration**: Optional integration with transformer models for improved accuracy

## Project Structure

```
/nlp
├── enhanced_language_model.py     # Core multilingual NLP implementation
├── training_data_generator.py     # Generates training data for ML models
├── model_evaluation.py            # Evaluates model performance
├── chatbot_integration.py         # Integration with WhatsApp chatbot
├── intent_handler.py              # English intent recognition and entity extraction
├── hindi_support.py               # Hindi intent recognition and entity extraction
├── improved_language_detection.py # Enhanced language detection
├── integrated_improvements_test.py # Test script for integrated improvements
├── requirements.txt               # Project dependencies
└── README_MULTILINGUAL.md         # This documentation
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download required spaCy models:

```bash
python -m spacy download en_core_web_md
python -m spacy download xx_ent_wiki_sm
```

## Usage

### Basic Usage

To process a user message and get a response:

```python
from chatbot_integration import ChatbotIntegration

# Initialize chatbot
chatbot = ChatbotIntegration()

# Process a message
response = chatbot.process_message("Show me my inventory", "user123")
print(response)

# Process a Hindi message
response = chatbot.process_message("मेरा इन्वेंटरी दिखाओ", "user123")
print(response)

# Process a mixed language message
response = chatbot.process_message("Show me चावल inventory", "user123")
print(response)
```

### Using the Enhanced Language Model Directly

```python
from enhanced_language_model import parse_multilingual_command

# Parse a command
result = parse_multilingual_command("Update rice stock to 50")
print(result)

# Result contains:
# - language: detected language ("en", "hi")
# - is_mixed_language: whether the message contains mixed languages
# - intent: recognized intent (e.g., "edit_stock")
# - confidence: confidence score for intent recognition
# - entities: extracted entities (e.g., {"product_name": "rice", "stock": 50})
```

### Generating Training Data

To generate training data for ML models:

```bash
python training_data_generator.py
```

This will create training and testing datasets in the `./data` directory.

### Evaluating Model Performance

To evaluate the model's performance:

```bash
python model_evaluation.py
```

This will generate evaluation metrics and visualizations in the `./evaluation_results` directory.

## Supported Intents

The system supports the following intents in both English and Hindi:

1. `get_inventory` - View current inventory
2. `get_low_stock` - View products with low stock
3. `get_report` - Generate sales reports
4. `get_top_products` - View top-selling products
5. `get_customer_data` - View customer analytics
6. `add_product` - Add a new product
7. `edit_stock` - Update product stock
8. `get_orders` - View orders
9. `search_product` - Search for products

## Language Detection

The system uses a hybrid approach for language detection:

1. **Character Frequency Analysis**: Analyzes the frequency of Hindi and English characters
2. **Mixed Language Detection**: Identifies messages containing significant portions of both languages
3. **Confidence Scoring**: Provides confidence levels for language detection

## Intent Recognition

The system uses a hybrid approach for intent recognition:

1. **Rule-Based Patterns**: Uses regex patterns for both English and Hindi
2. **ML-Based Classification**: Optional transformer model for improved accuracy
3. **Fallback Mechanism**: Falls back to alternative language patterns if primary language fails

## Entity Extraction

The system extracts various entities based on the recognized intent:

1. **Product Names**: For add_product, edit_stock, search_product intents
2. **Quantities**: Stock levels, thresholds, limits
3. **Prices**: For add_product intent
4. **Time Ranges**: For reports, orders, top products
5. **Date Ranges**: Custom date ranges for reports

## Extending the System

### Adding New Intents

To add a new intent:

1. Add regex patterns to `INTENT_PATTERNS` in `intent_handler.py` for English
2. Add regex patterns to `HINDI_INTENT_PATTERNS` in `hindi_support.py` for Hindi
3. Create entity extraction functions for the new intent
4. Update the `extract_entities` function in `enhanced_language_model.py`
5. Add response templates in `chatbot_integration.py`

### Adding New Languages

To add support for a new language:

1. Define character ranges for the new language
2. Create intent patterns for the new language
3. Implement entity extraction functions for the new language
4. Update language detection logic to include the new language
5. Add response templates for the new language

### Improving ML Model

To improve the ML-based intent classification:

1. Generate more training data with diverse examples
2. Train the transformer model using the `train_intent_classifier` function
3. Adjust confidence thresholds in the `recognize_intent` function

## Performance Optimization

For production deployment, consider the following optimizations:

1. **Lazy Loading**: The transformer model is loaded only when needed
2. **Caching**: Implement caching for frequently used patterns and responses
3. **Batch Processing**: Process multiple messages in batch for improved throughput
4. **Model Quantization**: Use quantized models for reduced memory footprint

## Testing

The system includes comprehensive testing capabilities:

1. **Unit Tests**: Test individual components (language detection, intent recognition, entity extraction)
2. **Integration Tests**: Test the entire pipeline with various inputs
3. **Evaluation Metrics**: Calculate accuracy, precision, recall, and F1 score
4. **Visualization**: Generate confusion matrices and accuracy charts

## API Integration

The system integrates with backend APIs for processing commands:

1. **API Endpoints**: Defined in `chatbot_integration.py`
2. **Parameter Formatting**: Converts extracted entities to API parameters
3. **Response Formatting**: Formats API responses into user-friendly messages
4. **Error Handling**: Handles API errors and provides appropriate responses

## Future Enhancements

1. **Additional Languages**: Support for more Indian languages
2. **Voice Input**: Integration with speech recognition
3. **Context Awareness**: Maintain conversation context for follow-up queries
4. **Sentiment Analysis**: Detect user sentiment for improved responses
5. **Active Learning**: Continuously improve models based on user interactions

## Troubleshooting

### Common Issues

1. **Missing spaCy Models**: Ensure you've downloaded the required models
2. **Memory Issues**: Reduce model size or implement lazy loading
3. **Performance Issues**: Use rule-based approach for time-sensitive applications
4. **Accuracy Issues**: Generate more training data for problematic intents

### Debugging

The system includes logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributors

- One Tappe Development Team

## License

Proprietary - All rights reserved