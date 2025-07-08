# Test Data Management Plan for NLP Command System

## Overview

This document outlines a comprehensive test data management strategy for the multilingual NLP command system. Effective test data management is crucial for ensuring consistent, reliable, and representative test execution across all testing phases. Given the complexity of natural language processing and the multilingual nature of the system, proper test data management is essential for thorough testing and quality assurance.

## Goals and Objectives

### Primary Goals

1. **Ensure Test Consistency**: Provide consistent test data across all testing environments and phases
2. **Support Comprehensive Testing**: Ensure test data covers all required scenarios and edge cases
3. **Maintain Data Quality**: Establish processes for creating and maintaining high-quality test data
4. **Enable Test Automation**: Provide test data in formats suitable for automated testing
5. **Protect Sensitive Information**: Ensure proper handling of any sensitive or personal information

### Specific Objectives

1. Create representative test data for all supported intents and entities
2. Develop multilingual test data sets for both English and Hindi
3. Establish processes for test data versioning and management
4. Define standards for test data documentation
5. Implement secure handling of test data containing sensitive information

## Test Data Requirements

### 1. Command Test Data

**Purpose**: Test data for NLP intent recognition and entity extraction

**Requirements**:
- Cover all supported intents (search_product, get_report, get_orders, get_inventory, get_top_products, etc.)
- Include variations in command phrasing for each intent
- Provide commands in both English and Hindi
- Include edge cases such as ambiguous commands, commands with spelling errors, etc.
- Cover all entity types (product names, categories, time periods, quantities, etc.)

**Example Structure**:
```json
{
  "intent": "search_product",
  "language": "english",
  "variations": [
    {
      "text": "search for red t-shirt",
      "entities": {
        "product_name": "red t-shirt"
      },
      "expected_intent_confidence": 0.95
    },
    {
      "text": "find red t-shirt in my inventory",
      "entities": {
        "product_name": "red t-shirt"
      },
      "expected_intent_confidence": 0.92
    },
    {
      "text": "do I have any red t-shirts",
      "entities": {
        "product_name": "red t-shirts"
      },
      "expected_intent_confidence": 0.85
    }
  ]
}
```

### 2. Mock API Response Data

**Purpose**: Test data for simulating backend API responses

**Requirements**:
- Cover all API endpoints used by the system
- Include both success and error responses
- Provide realistic data structures and values
- Include edge cases such as empty results, large result sets, etc.

**Example Structure**:
```json
{
  "endpoint": "/api/inventory/search",
  "responses": {
    "success": {
      "status": 200,
      "body": {
        "products": [
          {
            "id": "P12345",
            "name": "Red T-Shirt",
            "category": "Apparel",
            "quantity": 25,
            "price": 499.00
          },
          {
            "id": "P12346",
            "name": "Red Polo T-Shirt",
            "category": "Apparel",
            "quantity": 15,
            "price": 699.00
          }
        ],
        "total": 2
      }
    },
    "empty": {
      "status": 200,
      "body": {
        "products": [],
        "total": 0
      }
    },
    "error": {
      "status": 500,
      "body": {
        "error": "Internal server error",
        "message": "Unable to connect to database"
      }
    }
  }
}
```

### 3. User Profile Test Data

**Purpose**: Test data for simulating different user contexts

**Requirements**:
- Cover different user types (new users, experienced users, etc.)
- Include users with different language preferences
- Provide realistic user metadata
- Include edge cases such as users with minimal history, users with extensive history, etc.

**Example Structure**:
```json
{
  "user_id": "U12345",
  "phone_number": "+919876543210",
  "language_preference": "hindi",
  "business_type": "Clothing Store",
  "account_age_days": 120,
  "session_history": [
    {
      "timestamp": "2023-05-01T10:15:30Z",
      "command": "मेरा इन्वेंटरी दिखाओ",
      "intent": "get_inventory"
    },
    {
      "timestamp": "2023-05-02T14:22:45Z",
      "command": "पिछले हफ्ते की बिक्री रिपोर्ट",
      "intent": "get_report"
    }
  ]
}
```

### 4. WhatsApp Message Test Data

**Purpose**: Test data for simulating WhatsApp message events

**Requirements**:
- Cover different message types (text, media, etc.)
- Include messages in both English and Hindi
- Provide realistic message metadata
- Include edge cases such as very long messages, messages with special characters, etc.

**Example Structure**:
```json
{
  "message_id": "wamid.abcd1234",
  "from": "+919876543210",
  "timestamp": "2023-05-03T09:45:22Z",
  "type": "text",
  "text": {
    "body": "show me my inventory status"
  },
  "context": {
    "from": "917654321098",
    "id": "wamid.efgh5678"
  }
}
```

## Test Data Organization

### Directory Structure

```
test_data/
├── commands/
│   ├── english/
│   │   ├── search_product.json
│   │   ├── get_report.json
│   │   ├── get_orders.json
│   │   ├── get_inventory.json
│   │   └── get_top_products.json
│   └── hindi/
│       ├── search_product.json
│       ├── get_report.json
│       ├── get_orders.json
│       ├── get_inventory.json
│       └── get_top_products.json
├── api_responses/
│   ├── inventory_api.json
│   ├── order_api.json
│   ├── product_api.json
│   └── report_api.json
├── user_profiles/
│   ├── new_users.json
│   ├── experienced_users.json
│   ├── hindi_users.json
│   └── english_users.json
└── whatsapp_messages/
    ├── text_messages.json
    ├── media_messages.json
    └── system_messages.json
```

### Naming Conventions

- **Files**: Use lowercase with underscores, descriptive names
- **Test Data IDs**: Use prefixes to indicate data type (e.g., CMD_ for commands, API_ for API responses)
- **Variations**: Use suffixes to indicate variations (e.g., _success, _error, _empty)

## Test Data Creation and Maintenance

### 1. Test Data Creation Process

#### Manual Creation

1. Identify test scenarios requiring test data
2. Define the structure and content of required test data
3. Create test data files according to defined structure
4. Review test data for completeness and accuracy
5. Commit test data to version control

#### Automated Generation

1. Define templates for different types of test data
2. Implement data generation scripts
3. Configure generation parameters (e.g., number of variations, languages)
4. Execute generation scripts
5. Validate generated data
6. Commit generated data to version control

### 2. Test Data Versioning

- Use version control system (Git) for test data
- Tag test data versions to align with application versions
- Document changes to test data in commit messages
- Maintain backward compatibility when possible

### 3. Test Data Validation

- Implement schema validation for test data files
- Validate test data during CI/CD pipeline
- Check for required fields and data types
- Verify referential integrity between related data sets

### 4. Test Data Refresh

- Schedule regular reviews of test data
- Update test data to reflect changes in application requirements
- Add new test data for new features or scenarios
- Archive obsolete test data

## Test Data Usage

### 1. In Unit Tests

```python
# Example of using test data in a unit test
import json
import unittest
from nlp.intent_recognizer import IntentRecognizer

class TestIntentRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = IntentRecognizer()
        # Load test data
        with open('test_data/commands/english/search_product.json', 'r') as f:
            self.test_data = json.load(f)
    
    def test_search_product_intent_recognition(self):
        for variation in self.test_data['variations']:
            command = variation['text']
            expected_intent = self.test_data['intent']
            expected_confidence = variation['expected_intent_confidence']
            
            result = self.recognizer.recognize_intent(command)
            
            self.assertEqual(result['intent'], expected_intent)
            self.assertGreaterEqual(result['confidence'], expected_confidence)
```

### 2. In Integration Tests

```python
# Example of using test data in an integration test
import json
import unittest
from unittest.mock import patch
from nlp.command_router import CommandRouter

class TestCommandRouter(unittest.TestCase):
    def setUp(self):
        self.router = CommandRouter()
        # Load command test data
        with open('test_data/commands/english/search_product.json', 'r') as f:
            self.command_data = json.load(f)
        # Load API response test data
        with open('test_data/api_responses/product_api.json', 'r') as f:
            self.api_data = json.load(f)
    
    @patch('nlp.api_client.ProductAPI.search')
    def test_search_product_routing(self, mock_search):
        # Configure mock to return test API response
        mock_search.return_value = self.api_data['responses']['success']
        
        # Use test command
        command = self.command_data['variations'][0]['text']
        expected_product_name = self.command_data['variations'][0]['entities']['product_name']
        
        # Execute command routing
        response = self.router.route_command(command)
        
        # Verify API was called with correct parameters
        mock_search.assert_called_once_with(product_name=expected_product_name)
        
        # Verify response contains expected data
        self.assertIn('products', response)
        self.assertEqual(len(response['products']), 2)
```

### 3. In System Tests

```python
# Example of using test data in a system test
import json
import unittest
from unittest.mock import patch
from nlp.whatsapp_handler import WhatsAppHandler

class TestWhatsAppIntegration(unittest.TestCase):
    def setUp(self):
        self.handler = WhatsAppHandler()
        # Load WhatsApp message test data
        with open('test_data/whatsapp_messages/text_messages.json', 'r') as f:
            self.message_data = json.load(f)
        # Load user profile test data
        with open('test_data/user_profiles/hindi_users.json', 'r') as f:
            self.user_data = json.load(f)
        # Load API response test data
        with open('test_data/api_responses/inventory_api.json', 'r') as f:
            self.api_data = json.load(f)
    
    @patch('nlp.api_client.InventoryAPI.get_status')
    @patch('nlp.whatsapp_client.send_message')
    def test_end_to_end_flow(self, mock_send, mock_get_status):
        # Configure mocks
        mock_get_status.return_value = self.api_data['responses']['success']
        
        # Create test message
        message = self.message_data[0]  # Get first test message
        message['from'] = self.user_data['phone_number']  # Use phone number from user profile
        
        # Process the message
        self.handler.process_message(message)
        
        # Verify WhatsApp response was sent
        mock_send.assert_called_once()
        sent_message = mock_send.call_args[0][0]
        
        # Verify response content
        self.assertIn('inventory status', sent_message['text']['body'].lower())
```

## Test Data Security

### 1. Sensitive Data Handling

- Avoid using real customer data in test data sets
- If real data must be used, ensure proper anonymization
- Use data masking techniques for sensitive fields
- Implement access controls for test data containing sensitive information

### 2. Data Masking Techniques

- **Substitution**: Replace sensitive values with fictional but realistic values
- **Shuffling**: Rearrange data within a column to break the association with other columns
- **Encryption**: Encrypt sensitive fields while maintaining format
- **Generalization**: Replace specific values with more general ones

### 3. Compliance Considerations

- Ensure test data handling complies with relevant regulations (e.g., GDPR, CCPA)
- Document data handling procedures for audit purposes
- Regularly review and update data handling practices
- Provide training on proper handling of sensitive test data

## Test Data for Specific Testing Types

### 1. Regression Testing

- Maintain a core set of test data covering critical functionality
- Version this data set to align with application releases
- Include test data for previously identified and fixed issues
- Ensure consistency of this data set across test environments

### 2. Performance Testing

- Create larger volumes of test data for load testing
- Include test data with varying complexity
- Generate test data that simulates peak usage patterns
- Include test data for measuring specific performance metrics

### 3. Security Testing

- Create test data with potential security vulnerabilities
- Include test data for testing input validation
- Develop test data for authentication and authorization testing
- Include test data for testing data protection mechanisms

### 4. Usability Testing

- Create realistic test scenarios with corresponding test data
- Include test data representing different user personas
- Develop test data for common user workflows
- Include test data for edge cases and error scenarios

## Test Data Management Tools

### 1. Version Control

- **Git**: For versioning test data files
- **GitHub/GitLab**: For collaborative management of test data

### 2. Data Generation

- **Faker**: For generating realistic fake data
- **Custom scripts**: For domain-specific test data generation

### 3. Data Validation

- **JSON Schema**: For validating JSON test data structure
- **PyTest**: For validating test data during test execution

### 4. Data Storage

- **File System**: For simple test data storage
- **Database**: For more complex or relational test data

## Implementation Plan

### Phase 1: Initial Setup (Weeks 1-2)

1. Define test data requirements for each component
2. Design test data structures and formats
3. Set up test data directory structure
4. Implement basic validation mechanisms

### Phase 2: Core Test Data Creation (Weeks 3-4)

1. Create test data for core intents and entities
2. Develop test data for critical API responses
3. Create basic user profiles
4. Implement initial WhatsApp message test data

### Phase 3: Comprehensive Test Data (Weeks 5-6)

1. Expand test data to cover all intents and entities
2. Create test data for edge cases and error scenarios
3. Develop multilingual test data sets
4. Implement test data for performance testing

### Phase 4: Automation and Integration (Weeks 7-8)

1. Develop test data generation scripts
2. Integrate test data with CI/CD pipeline
3. Implement test data refresh processes
4. Document test data usage and management

## Test Data Documentation

### 1. Test Data Catalog

Maintain a catalog of available test data sets with the following information:

- Test data set name and location
- Purpose and intended use cases
- Structure and format
- Coverage (features, scenarios, etc.)
- Dependencies on other test data sets
- Version information

### 2. Usage Guidelines

Provide guidelines for using test data effectively:

- How to select appropriate test data for different test types
- How to extend or customize existing test data
- Best practices for test data management
- Troubleshooting common issues

### 3. Maintenance Procedures

Document procedures for maintaining test data:

- How to update test data for new features
- How to version test data
- How to validate test data
- How to archive obsolete test data

## Conclusion

This test data management plan provides a comprehensive approach to creating, maintaining, and using test data for the multilingual NLP command system. By implementing this plan, we can ensure that testing is based on consistent, high-quality test data that covers all required scenarios and edge cases.

Effective test data management is essential for thorough testing and quality assurance of the NLP command system. This plan establishes the processes and standards needed to achieve this goal, supporting both manual and automated testing efforts across all testing phases.

## Appendices

### Appendix A: Sample Test Data Files

#### A.1: Sample Command Test Data (English)

```json
{
  "intent": "get_inventory",
  "language": "english",
  "variations": [
    {
      "text": "show me my inventory",
      "entities": {},
      "expected_intent_confidence": 0.95
    },
    {
      "text": "check inventory status",
      "entities": {},
      "expected_intent_confidence": 0.92
    },
    {
      "text": "what's in my inventory",
      "entities": {},
      "expected_intent_confidence": 0.88
    },
    {
      "text": "show inventory for electronics",
      "entities": {
        "category": "electronics"
      },
      "expected_intent_confidence": 0.90
    },
    {
      "text": "show top 10 items in inventory",
      "entities": {
        "limit": 10
      },
      "expected_intent_confidence": 0.85
    }
  ]
}
```

#### A.2: Sample Command Test Data (Hindi)

```json
{
  "intent": "get_inventory",
  "language": "hindi",
  "variations": [
    {
      "text": "मेरा इन्वेंटरी दिखाओ",
      "entities": {},
      "expected_intent_confidence": 0.92
    },
    {
      "text": "इन्वेंटरी स्टेटस चेक करो",
      "entities": {},
      "expected_intent_confidence": 0.90
    },
    {
      "text": "मेरे इन्वेंटरी में क्या है",
      "entities": {},
      "expected_intent_confidence": 0.85
    },
    {
      "text": "इलेक्ट्रॉनिक्स का इन्वेंटरी दिखाओ",
      "entities": {
        "category": "इलेक्ट्रॉनिक्स"
      },
      "expected_intent_confidence": 0.88
    },
    {
      "text": "इन्वेंटरी में टॉप 10 आइटम दिखाओ",
      "entities": {
        "limit": 10
      },
      "expected_intent_confidence": 0.82
    }
  ]
}
```

#### A.3: Sample API Response Test Data

```json
{
  "endpoint": "/api/inventory/status",
  "responses": {
    "success": {
      "status": 200,
      "body": {
        "total_items": 156,
        "categories": [
          {
            "name": "Apparel",
            "count": 78,
            "value": 156000.00
          },
          {
            "name": "Electronics",
            "count": 45,
            "value": 225000.00
          },
          {
            "name": "Home Goods",
            "count": 33,
            "value": 82500.00
          }
        ],
        "low_stock_items": 12,
        "out_of_stock_items": 3
      }
    },
    "empty": {
      "status": 200,
      "body": {
        "total_items": 0,
        "categories": [],
        "low_stock_items": 0,
        "out_of_stock_items": 0
      }
    },
    "error": {
      "status": 500,
      "body": {
        "error": "Internal server error",
        "message": "Unable to retrieve inventory status"
      }
    }
  }
}
```

### Appendix B: Test Data Generation Script Example

```python
#!/usr/bin/env python3

"""
Test data generator for NLP command system.

This script generates test data for various intents in both English and Hindi.
"""

import json
import os
import random
from typing import Dict, List, Any

# Define base templates for commands
ENGLISH_TEMPLATES = {
    "search_product": [
        "search for {product}",
        "find {product}",
        "do you have {product}",
        "check if {product} is available",
        "look for {product} in inventory"
    ],
    "get_inventory": [
        "show me my inventory",
        "check inventory status",
        "what's in my inventory",
        "show inventory for {category}",
        "show top {limit} items in inventory"
    ],
    # Add more intent templates as needed
}

HINDI_TEMPLATES = {
    "search_product": [
        "{product} खोजें",
        "{product} ढूंढें",
        "क्या आपके पास {product} है",
        "चेक करें कि {product} उपलब्ध है",
        "इन्वेंटरी में {product} देखें"
    ],
    "get_inventory": [
        "मेरा इन्वेंटरी दिखाओ",
        "इन्वेंटरी स्टेटस चेक करो",
        "मेरे इन्वेंटरी में क्या है",
        "{category} का इन्वेंटरी दिखाओ",
        "इन्वेंटरी में टॉप {limit} आइटम दिखाओ"
    ],
    # Add more intent templates as needed
}

# Define entity values
ENTITY_VALUES = {
    "product": [
        "red t-shirt", "blue jeans", "black shoes", "white socks", "green hat",
        "smartphone", "laptop", "headphones", "smart watch", "tablet"
    ],
    "category": [
        "apparel", "electronics", "home goods", "accessories", "footwear"
    ],
    "limit": [5, 10, 15, 20, 25]
}

HINDI_ENTITY_VALUES = {
    "product": [
        "लाल टी-शर्ट", "नीली जींस", "काले जूते", "सफेद मोजे", "हरी टोपी",
        "स्मार्टफोन", "लैपटॉप", "हेडफोन", "स्मार्ट वॉच", "टैबलेट"
    ],
    "category": [
        "कपड़े", "इलेक्ट्रॉनिक्स", "घरेलू सामान", "एक्सेसरीज", "जूते"
    ],
    "limit": [5, 10, 15, 20, 25]
}

def generate_command_variations(intent: str, language: str, count: int = 5) -> Dict[str, Any]:
    """
    Generate command variations for a specific intent and language.
    
    Args:
        intent: The intent to generate commands for
        language: The language to generate commands in (english or hindi)
        count: Number of variations to generate
        
    Returns:
        Dictionary containing intent, language, and variations
    """
    templates = ENGLISH_TEMPLATES if language == "english" else HINDI_TEMPLATES
    entity_values = ENTITY_VALUES if language == "english" else HINDI_ENTITY_VALUES
    
    if intent not in templates:
        raise ValueError(f"Intent {intent} not supported")
    
    variations = []
    for i in range(count):
        # Select a random template
        template = random.choice(templates[intent])
        
        # Identify entities in the template
        entities = {}
        for entity_type in entity_values.keys():
            if f"{{{entity_type}}}" in template:
                entity_value = random.choice(entity_values[entity_type])
                entities[entity_type] = entity_value
                template = template.replace(f"{{{entity_type}}}", str(entity_value))
        
        # Calculate expected confidence (slightly randomized but high)
        confidence = round(random.uniform(0.80, 0.98), 2)
        
        variations.append({
            "text": template,
            "entities": entities,
            "expected_intent_confidence": confidence
        })
    
    return {
        "intent": intent,
        "language": language,
        "variations": variations
    }

def save_test_data(data: Dict[str, Any], output_dir: str, filename: str) -> None:
    """
    Save test data to a JSON file.
    
    Args:
        data: The test data to save
        output_dir: Directory to save the file in
        filename: Name of the file to save
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated test data saved to {output_path}")

def main():
    """
    Main function to generate test data for all intents and languages.
    """
    # Define intents to generate data for
    intents = ["search_product", "get_inventory"]
    languages = ["english", "hindi"]
    
    # Create base output directory
    base_dir = "test_data/commands"
    
    # Generate test data for each intent and language
    for intent in intents:
        for language in languages:
            data = generate_command_variations(intent, language, count=10)
            output_dir = os.path.join(base_dir, language)
            filename = f"{intent}.json"
            save_test_data(data, output_dir, filename)

if __name__ == "__main__":
    main()
```

### Appendix C: Test Data Validation Schema Example

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Command Test Data",
  "type": "object",
  "required": ["intent", "language", "variations"],
  "properties": {
    "intent": {
      "type": "string",
      "enum": ["search_product", "get_report", "get_orders", "get_inventory", "get_top_products"]
    },
    "language": {
      "type": "string",
      "enum": ["english", "hindi"]
    },
    "variations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["text", "entities", "expected_intent_confidence"],
        "properties": {
          "text": {
            "type": "string",
            "minLength": 1
          },
          "entities": {
            "type": "object"
          },
          "expected_intent_confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        }
      },
      "minItems": 1
    }
  }
}
```