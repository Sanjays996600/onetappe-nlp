# One Tappe NLP System

This module provides multilingual NLP capabilities for the One Tappe WhatsApp Command Console, enabling the system to interpret seller messages in both English and Hindi, and route them to appropriate backend API endpoints.

## Overview

The NLP system uses a rule-based approach with regex pattern matching to identify commands and extract relevant entities. It supports both English and Hindi languages and includes a command router to connect NLP output to backend API calls.

The system currently supports the following intents:

- `get_inventory`: Show/list products
- `get_low_stock`: Show items with low stock
- `get_report`: Generate reports (today/week/month)
- `add_product`: Add new products with name, price, and stock
- `edit_stock`: Update stock levels for existing products
- `get_orders`: View order information

## Usage

### Basic Intent Recognition

```python
from nlp.multilingual_handler import parse_multilingual_command

# Parse an English command
result = parse_multilingual_command("Show my products")
# Returns: {"intent": "get_inventory", "entities": {}, "language": "en"}

# Parse a Hindi command
result = parse_multilingual_command("नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो")
# Returns: {"intent": "add_product", "entities": {"name": "चावल", "price": 50, "stock": 20}, "language": "hi"}
```

### End-to-End Command Processing

```python
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

# Process a command end-to-end
command = "Add new product Rice 50rs 20qty"
user_id = "seller_123"

# Parse the command
parsed_result = parse_multilingual_command(command)

# Route to backend API and get formatted response
response = route_command(parsed_result, user_id)
# Returns: "Product Rice added successfully with price ₹50 and stock 20."
```

## Testing

### Intent Recognition Testing

Run the comprehensive test script to verify intent recognition:

```bash
python -m nlp.comprehensive_test
```

This will run through various test cases in both English and Hindi and report success/failure statistics.

### End-to-End Testing

Test the complete flow from natural language to API response:

```bash
python -m nlp.test_command_router
```

This will process various commands in both languages and show the formatted responses.

## System Components

### Intent Handler (`intent_handler.py`)
- Handles English command parsing
- Contains regex patterns for intent recognition
- Provides entity extraction functions for various intents

### Hindi Support (`hindi_support.py`)
- Handles Hindi command parsing
- Contains Hindi-specific regex patterns for intent recognition
- Provides entity extraction functions tailored for Hindi language

### Multilingual Handler (`multilingual_handler.py`)
- Integrates English and Hindi language support
- Detects language and routes to appropriate parser
- Provides a unified interface for multilingual command processing

### Command Router (`command_router.py`)
- Maps NLP output to backend API calls
- Handles API request formatting and response processing
- Provides localized responses in the user's language

## API Integration

The command router maps intents to the following API endpoints:

| Intent | API Endpoint | Method | Parameters |
|--------|-------------|--------|------------|
| add_product | /seller/products/add | POST | name, price, stock |
| edit_stock | /seller/products/update-stock | POST | name, stock |
| get_inventory | /seller/products | GET | - |
| get_low_stock | /seller/products/low-stock | GET | - |
| get_report | /seller/report | GET | range |
| get_orders | /seller/orders | GET | - |

## Future Expansion

### ML/NLU Integration

To enhance the system with machine learning:

1. Install the required dependencies from `requirements.txt`
2. Collect training data from user interactions
3. Implement one of the following approaches:
   - Fine-tune a pre-trained model using transformers
   - Train a custom spaCy pipeline
   - Use a hybrid approach combining rules and ML

### Additional Languages

The system can be extended to support more Indian languages by:
1. Creating language-specific intent and entity extraction modules
2. Enhancing the language detection function
3. Adding language-specific response templates

### Confidence Scoring

Future versions will include confidence scores for intent recognition, allowing the system to request clarification when uncertain.

## Directory Structure

```
nlp/
├── __init__.py
├── intent_handler.py       # English intent recognition logic
├── hindi_support.py        # Hindi intent recognition logic
├── multilingual_handler.py # Language detection and routing
├── command_router.py       # API integration and response formatting
├── comprehensive_test.py   # Comprehensive test suite
├── test_command_router.py  # End-to-end testing
├── requirements.txt        # NLP library dependencies
└── README.md               # Documentation
```

## Integration with WhatsApp Bot

To integrate with the WhatsApp Bot:

1. Receive user messages from WhatsApp
2. Process the message using `parse_multilingual_command()`
3. Route the parsed result to backend APIs using `route_command()`
4. Send the formatted response back to the user via WhatsApp

Example flow:

```python
# In WhatsApp bot handler
def handle_whatsapp_message(message, user_id):
    # Parse the message
    parsed_result = parse_multilingual_command(message)
    
    # Route to backend API and get formatted response
    response = route_command(parsed_result, user_id)
    
    # Send response back to WhatsApp
    send_whatsapp_message(user_id, response)
```