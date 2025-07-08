# Test Automation Framework Design for NLP Command System

## Overview

This document outlines the design of a comprehensive test automation framework for the multilingual NLP command system. The framework aims to provide a structured, maintainable, and scalable approach to automated testing, enabling efficient verification of system functionality, performance, and reliability across both English and Hindi language interfaces.

## Goals and Objectives

### Primary Goals

1. **Increase Test Coverage**: Automate testing of all critical system components and user flows
2. **Improve Test Efficiency**: Reduce manual testing effort and execution time
3. **Enhance Test Reliability**: Create consistent, repeatable tests with minimal flakiness
4. **Support Multilingual Testing**: Enable automated testing in both English and Hindi
5. **Enable Continuous Testing**: Integrate with CI/CD pipeline for continuous feedback

### Specific Objectives

1. Design a modular, extensible test automation architecture
2. Implement reusable test components for common operations
3. Create a maintainable test data management system
4. Establish clear reporting and monitoring mechanisms
5. Support parallel test execution for improved efficiency
6. Enable cross-language testing with minimal duplication

## Framework Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Test Automation Framework                    │
├─────────────┬─────────────┬────────────────┬───────────────────┤
│  Test Cases │  Test Data  │ Page Objects/  │  Test Utilities   │
│             │ Management  │ Command Models │                   │
├─────────────┴─────────────┴────────────────┴───────────────────┤
│                        Test Execution Engine                    │
├─────────────┬─────────────┬────────────────┬───────────────────┤
│  Parallel   │  Reporting  │  Logging and   │  Configuration    │
│  Execution  │             │  Monitoring    │  Management       │
├─────────────┴─────────────┴────────────────┴───────────────────┤
│                        Test Integration Layer                   │
├─────────────┬─────────────┬────────────────┬───────────────────┤
│  WhatsApp   │  NLP Engine │  API Service   │  Database         │
│  Interface  │  Interface  │  Interface     │  Interface        │
└─────────────┴─────────────┴────────────────┴───────────────────┘
```

### Core Components

#### 1. Test Cases Layer

- **Intent Recognition Tests**: Verify correct identification of user intents
- **Entity Extraction Tests**: Verify extraction of entities from commands
- **Command Routing Tests**: Verify proper routing of commands to handlers
- **Integration Tests**: Verify end-to-end flows from command to response
- **Performance Tests**: Verify system performance under various conditions

#### 2. Test Data Management

- **Test Data Repository**: Centralized storage for test data
- **Data Generators**: Dynamic generation of test data
- **Data Providers**: Supply test data to test cases
- **Data Cleanup**: Clean up test data after test execution

#### 3. Page Objects / Command Models

- **Command Models**: Represent different command types and their properties
- **Response Models**: Represent expected responses for commands
- **Intent Models**: Represent intent recognition patterns
- **Entity Models**: Represent entity extraction patterns

#### 4. Test Utilities

- **Assertion Utilities**: Custom assertions for NLP-specific validations
- **Language Utilities**: Utilities for handling multilingual content
- **Mock Utilities**: Utilities for creating and managing mocks
- **Configuration Utilities**: Utilities for managing test configuration

#### 5. Test Execution Engine

- **Test Runner**: Execute test cases and manage test lifecycle
- **Parallel Execution**: Run tests in parallel for improved efficiency
- **Retry Mechanism**: Retry failed tests to handle flakiness
- **Test Filtering**: Select tests to run based on criteria

#### 6. Reporting and Monitoring

- **Test Reports**: Generate detailed test execution reports
- **Test Metrics**: Track test coverage, execution time, and other metrics
- **Failure Analysis**: Analyze and categorize test failures
- **Trend Analysis**: Track test metrics over time

#### 7. Test Integration Layer

- **WhatsApp Interface**: Interface with WhatsApp API for testing
- **NLP Engine Interface**: Interface with NLP engine for testing
- **API Service Interface**: Interface with backend APIs for testing
- **Database Interface**: Interface with database for data verification

## Technology Stack

### Core Technologies

- **Programming Language**: Python 3.9+
- **Testing Framework**: pytest
- **Mocking Framework**: unittest.mock, pytest-mock
- **Assertion Library**: pytest assertions, custom assertions

### Supporting Technologies

- **Continuous Integration**: GitHub Actions
- **Reporting**: pytest-html, Allure
- **Coverage Analysis**: pytest-cov
- **Performance Testing**: Locust
- **API Testing**: requests, pytest-httpx
- **Parallel Execution**: pytest-xdist

## Framework Implementation

### 1. Directory Structure

```
tests/
├── conftest.py                  # Common fixtures and configuration
├── test_data/                   # Test data files
│   ├── commands/                # Command test data
│   │   ├── english/             # English commands
│   │   └── hindi/               # Hindi commands
│   ├── responses/               # Expected responses
│   └── api_mocks/               # API mock responses
├── models/                      # Test models
│   ├── command_models.py        # Command representation models
│   ├── response_models.py       # Response representation models
│   ├── intent_models.py         # Intent representation models
│   └── entity_models.py         # Entity representation models
├── utilities/                   # Test utilities
│   ├── assertions.py            # Custom assertions
│   ├── language_utils.py        # Language handling utilities
│   ├── mock_utils.py            # Mocking utilities
│   └── config_utils.py          # Configuration utilities
├── fixtures/                    # Test fixtures
│   ├── api_fixtures.py          # API testing fixtures
│   ├── nlp_fixtures.py          # NLP testing fixtures
│   ├── whatsapp_fixtures.py     # WhatsApp testing fixtures
│   └── data_fixtures.py         # Data management fixtures
├── unit/                        # Unit tests
│   ├── test_intent_recognition.py  # Intent recognition tests
│   ├── test_entity_extraction.py   # Entity extraction tests
│   └── test_command_routing.py     # Command routing tests
├── integration/                 # Integration tests
│   ├── test_whatsapp_integration.py  # WhatsApp integration tests
│   ├── test_api_integration.py      # API integration tests
│   └── test_end_to_end.py           # End-to-end tests
└── performance/                 # Performance tests
    ├── test_response_time.py    # Response time tests
    ├── test_throughput.py       # Throughput tests
    └── locustfile.py            # Locust load testing configuration
```

### 2. Key Implementation Components

#### Test Fixtures

```python
# conftest.py
import pytest
from unittest.mock import patch
from nlp.intent_recognizer import IntentRecognizer
from nlp.entity_extractor import EntityExtractor
from nlp.command_router import CommandRouter

@pytest.fixture
def intent_recognizer():
    """Fixture for intent recognizer with mocked dependencies."""
    recognizer = IntentRecognizer()
    # Configure recognizer for testing
    return recognizer

@pytest.fixture
def entity_extractor():
    """Fixture for entity extractor with mocked dependencies."""
    extractor = EntityExtractor()
    # Configure extractor for testing
    return extractor

@pytest.fixture
def command_router():
    """Fixture for command router with mocked dependencies."""
    with patch('nlp.api_client.APIClient') as mock_api_client:
        router = CommandRouter(api_client=mock_api_client)
        yield router

@pytest.fixture
def load_test_commands(request):
    """Fixture to load test commands from files."""
    language = request.param.get('language', 'english')
    intent = request.param.get('intent', 'get_orders')
    
    # Load test commands from file
    file_path = f"tests/test_data/commands/{language}/{intent}.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        commands = json.load(f)
    
    return commands
```

#### Command Models

```python
# models/command_models.py
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Command:
    """Represents a user command for testing."""
    text: str
    language: str
    expected_intent: str
    expected_entities: Dict[str, Any]
    expected_confidence: float = 0.8
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert command to dictionary representation."""
        return {
            "text": self.text,
            "language": self.language,
            "expected_intent": self.expected_intent,
            "expected_entities": self.expected_entities,
            "expected_confidence": self.expected_confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Command':
        """Create command from dictionary representation."""
        return cls(
            text=data["text"],
            language=data["language"],
            expected_intent=data["expected_intent"],
            expected_entities=data["expected_entities"],
            expected_confidence=data.get("expected_confidence", 0.8)
        )
```

#### Custom Assertions

```python
# utilities/assertions.py
from typing import Dict, Any, List, Optional

def assert_intent_recognition(result: Dict[str, Any], expected_intent: str, 
                             min_confidence: float = 0.8) -> None:
    """Assert that intent recognition result matches expected intent."""
    assert "intent" in result, "Intent not found in result"
    assert result["intent"] == expected_intent, \
        f"Expected intent {expected_intent}, got {result['intent']}"
    
    assert "confidence" in result, "Confidence not found in result"
    assert result["confidence"] >= min_confidence, \
        f"Confidence {result['confidence']} below minimum {min_confidence}"

def assert_entity_extraction(result: Dict[str, Any], 
                            expected_entities: Dict[str, Any]) -> None:
    """Assert that entity extraction result matches expected entities."""
    assert "entities" in result, "Entities not found in result"
    
    for entity_name, expected_value in expected_entities.items():
        assert entity_name in result["entities"], \
            f"Entity {entity_name} not found in extracted entities"
        
        actual_value = result["entities"][entity_name]
        assert actual_value == expected_value, \
            f"Entity {entity_name}: expected {expected_value}, got {actual_value}"

def assert_command_response(response: Dict[str, Any], 
                           expected_content: List[str],
                           language: str = "english") -> None:
    """Assert that command response contains expected content."""
    assert "text" in response, "Text not found in response"
    
    for content in expected_content:
        assert content in response["text"], \
            f"Expected content '{content}' not found in response"
    
    if language == "english":
        assert response.get("language", "") == "english", \
            f"Expected language 'english', got {response.get('language', '')}"
    elif language == "hindi":
        assert response.get("language", "") == "hindi", \
            f"Expected language 'hindi', got {response.get('language', '')}"
```

#### Test Data Providers

```python
# utilities/data_providers.py
import json
from typing import Dict, Any, List, Generator
from models.command_models import Command

def provide_commands(language: str, intent: str) -> List[Command]:
    """Provide test commands for a specific language and intent."""
    file_path = f"tests/test_data/commands/{language}/{intent}.json"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    commands = []
    for item in data["variations"]:
        command = Command(
            text=item["text"],
            language=language,
            expected_intent=intent,
            expected_entities=item["entities"],
            expected_confidence=item.get("expected_intent_confidence", 0.8)
        )
        commands.append(command)
    
    return commands

def provide_api_responses(endpoint: str) -> Dict[str, Any]:
    """Provide mock API responses for a specific endpoint."""
    file_path = f"tests/test_data/api_mocks/{endpoint}.json"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        responses = json.load(f)
    
    return responses
```

### 3. Test Implementation Examples

#### Intent Recognition Tests

```python
# unit/test_intent_recognition.py
import pytest
from utilities.assertions import assert_intent_recognition
from utilities.data_providers import provide_commands

class TestIntentRecognition:
    """Tests for intent recognition functionality."""
    
    @pytest.mark.parametrize("language,intent", [
        ("english", "get_orders"),
        ("english", "get_inventory"),
        ("english", "get_top_products"),
        ("hindi", "get_orders"),
        ("hindi", "get_inventory"),
        ("hindi", "get_top_products")
    ])
    def test_intent_recognition(self, intent_recognizer, language, intent):
        """Test that intents are correctly recognized for various commands."""
        commands = provide_commands(language, intent)
        
        for command in commands:
            result = intent_recognizer.recognize_intent(command.text)
            assert_intent_recognition(
                result, 
                command.expected_intent, 
                command.expected_confidence
            )
    
    def test_ambiguous_intent(self, intent_recognizer):
        """Test handling of ambiguous commands."""
        ambiguous_command = "show me everything"
        result = intent_recognizer.recognize_intent(ambiguous_command)
        
        # Should return the most likely intent but with lower confidence
        assert "intent" in result
        assert "confidence" in result
        assert result["confidence"] < 0.8
    
    def test_unknown_intent(self, intent_recognizer):
        """Test handling of commands with unknown intent."""
        unknown_command = "abcdefghijklmnopqrstuvwxyz"
        result = intent_recognizer.recognize_intent(unknown_command)
        
        assert result["intent"] == "unknown"
        assert result["confidence"] < 0.5
```

#### Entity Extraction Tests

```python
# unit/test_entity_extraction.py
import pytest
from utilities.assertions import assert_entity_extraction
from utilities.data_providers import provide_commands

class TestEntityExtraction:
    """Tests for entity extraction functionality."""
    
    @pytest.mark.parametrize("language,intent", [
        ("english", "get_orders"),
        ("english", "get_inventory"),
        ("hindi", "get_orders"),
        ("hindi", "get_inventory")
    ])
    def test_entity_extraction(self, entity_extractor, language, intent):
        """Test that entities are correctly extracted from commands."""
        commands = provide_commands(language, intent)
        
        for command in commands:
            if not command.expected_entities:  # Skip commands with no expected entities
                continue
                
            result = entity_extractor.extract_entities(command.text, command.expected_intent)
            assert_entity_extraction(result, command.expected_entities)
    
    def test_time_period_extraction(self, entity_extractor):
        """Test extraction of time period entities."""
        test_cases = [
            {
                "command": "show orders from last week",
                "intent": "get_orders",
                "expected": {"time_period": "last_week"}
            },
            {
                "command": "show orders from yesterday",
                "intent": "get_orders",
                "expected": {"time_period": "yesterday"}
            },
            {
                "command": "पिछले हफ्ते के ऑर्डर दिखाओ",  # Show orders from last week in Hindi
                "intent": "get_orders",
                "expected": {"time_period": "last_week"}
            }
        ]
        
        for case in test_cases:
            result = entity_extractor.extract_entities(case["command"], case["intent"])
            assert_entity_extraction(result, case["expected"])
    
    def test_multiple_entity_extraction(self, entity_extractor):
        """Test extraction of multiple entities from a single command."""
        command = "show top 10 products from last month"
        intent = "get_top_products"
        expected_entities = {"limit": 10, "time_period": "last_month"}
        
        result = entity_extractor.extract_entities(command, intent)
        assert_entity_extraction(result, expected_entities)
```

#### Command Routing Tests

```python
# unit/test_command_routing.py
import pytest
from unittest.mock import patch, MagicMock
from utilities.assertions import assert_command_response
from utilities.data_providers import provide_commands, provide_api_responses

class TestCommandRouting:
    """Tests for command routing functionality."""
    
    @pytest.mark.parametrize("language,intent", [
        ("english", "get_orders"),
        ("hindi", "get_orders")
    ])
    def test_get_orders_routing(self, command_router, language, intent):
        """Test routing of get_orders commands."""
        commands = provide_commands(language, intent)
        api_responses = provide_api_responses("orders")
        
        # Configure mock API client
        command_router.api_client.get_orders.return_value = api_responses["responses"]["success"]
        
        for command in commands:
            response = command_router.route_command(command.text)
            
            # Verify API was called with correct parameters
            if "time_period" in command.expected_entities:
                command_router.api_client.get_orders.assert_called_with(
                    time_period=command.expected_entities["time_period"]
                )
            
            # Verify response contains expected content
            expected_content = ["orders", "found"] if language == "english" else ["ऑर्डर", "मिले"]
            assert_command_response(response, expected_content, language)
    
    def test_error_handling(self, command_router):
        """Test handling of API errors during command routing."""
        command = "show my orders"
        api_responses = provide_api_responses("orders")
        
        # Configure mock API client to return error
        command_router.api_client.get_orders.return_value = api_responses["responses"]["error"]
        
        response = command_router.route_command(command)
        
        # Verify error response
        assert "error" in response
        assert "text" in response
        assert "Sorry" in response["text"]
```

#### WhatsApp Integration Tests

```python
# integration/test_whatsapp_integration.py
import pytest
from unittest.mock import patch, MagicMock
from nlp.whatsapp_handler import WhatsAppHandler
from utilities.data_providers import provide_api_responses

class TestWhatsAppIntegration:
    """Tests for WhatsApp integration functionality."""
    
    @pytest.fixture
    def whatsapp_handler(self):
        """Fixture for WhatsApp handler with mocked dependencies."""
        with patch('nlp.command_router.CommandRouter') as mock_router, \
             patch('nlp.whatsapp_client.WhatsAppClient') as mock_client:
            handler = WhatsAppHandler(router=mock_router, client=mock_client)
            yield handler
    
    def test_message_processing(self, whatsapp_handler):
        """Test processing of WhatsApp messages."""
        # Create test message
        message = {
            "from": "+919876543210",
            "text": {"body": "show my orders"}
        }
        
        # Configure mock router to return a response
        response = {"text": "You have 5 orders.", "language": "english"}
        whatsapp_handler.router.route_command.return_value = response
        
        # Process the message
        whatsapp_handler.process_message(message)
        
        # Verify router was called with correct command
        whatsapp_handler.router.route_command.assert_called_once_with("show my orders")
        
        # Verify WhatsApp client was called to send response
        whatsapp_handler.client.send_message.assert_called_once()
        call_args = whatsapp_handler.client.send_message.call_args[0]
        assert call_args[0] == "+919876543210"  # Recipient
        assert call_args[1] == "You have 5 orders."  # Message text
    
    def test_error_handling(self, whatsapp_handler):
        """Test handling of errors during message processing."""
        # Create test message
        message = {
            "from": "+919876543210",
            "text": {"body": "show my orders"}
        }
        
        # Configure mock router to raise an exception
        whatsapp_handler.router.route_command.side_effect = Exception("Test error")
        
        # Process the message
        whatsapp_handler.process_message(message)
        
        # Verify WhatsApp client was called to send error response
        whatsapp_handler.client.send_message.assert_called_once()
        call_args = whatsapp_handler.client.send_message.call_args[0]
        assert call_args[0] == "+919876543210"  # Recipient
        assert "sorry" in call_args[1].lower()  # Error message
```

### 4. Performance Testing

```python
# performance/locustfile.py
from locust import HttpUser, task, between
import json

class NLPUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Setup before starting tests."""
        # Load test commands
        with open("tests/test_data/commands/english/get_orders.json", "r") as f:
            self.commands = json.load(f)["variations"]
    
    @task(3)
    def test_get_orders(self):
        """Test get_orders intent performance."""
        command = self.commands[0]["text"]
        self.client.post("/api/process_command", json={"command": command})
    
    @task(2)
    def test_get_inventory(self):
        """Test get_inventory intent performance."""
        with open("tests/test_data/commands/english/get_inventory.json", "r") as f:
            commands = json.load(f)["variations"]
        command = commands[0]["text"]
        self.client.post("/api/process_command", json={"command": command})
    
    @task(1)
    def test_get_top_products(self):
        """Test get_top_products intent performance."""
        with open("tests/test_data/commands/english/get_top_products.json", "r") as f:
            commands = json.load(f)["variations"]
        command = commands[0]["text"]
        self.client.post("/api/process_command", json={"command": command})
```

## Test Execution

### 1. Running Tests

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_intent_recognition.py

# Run tests with specific marker
pytest -m "english"

# Run tests in parallel
pytest -xvs -n 4

# Generate HTML report
pytest --html=report.html

# Run with coverage
pytest --cov=nlp
```

### 2. Test Configuration

```python
# pytest.ini
[pytest]
markers =
    english: Tests for English language
    hindi: Tests for Hindi language
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = -v --strict-markers
```

### 3. CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Automation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-html pytest-xdist
    
    - name: Run unit tests
      run: pytest tests/unit/ -v --cov=nlp --cov-report=xml
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
    
    - name: Upload coverage report
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
    
    - name: Generate HTML report
      run: pytest --html=test-report.html
    
    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: test-report.html
```

## Test Reporting and Monitoring

### 1. Test Reports

- **HTML Reports**: Generate detailed HTML reports with pytest-html
- **Coverage Reports**: Generate coverage reports with pytest-cov
- **Allure Reports**: Generate interactive reports with Allure

### 2. Test Metrics

- **Test Coverage**: Percentage of code covered by tests
- **Test Pass Rate**: Percentage of tests that pass
- **Test Execution Time**: Time taken to execute tests
- **Test Flakiness**: Percentage of tests that fail intermittently

### 3. Test Monitoring

- **CI/CD Integration**: Monitor test results in CI/CD pipeline
- **Trend Analysis**: Track test metrics over time
- **Failure Analysis**: Analyze and categorize test failures
- **Alert System**: Alert on test failures or regressions

## Multilingual Testing Strategy

### 1. Language-Specific Test Data

- Maintain separate test data files for each supported language
- Use consistent structure across language-specific test data
- Include language-specific variations and edge cases

### 2. Language Detection Tests

- Test accurate detection of command language
- Verify correct language-specific processing
- Test handling of mixed-language commands

### 3. Translation Verification

- Verify correct translation of responses
- Test language-specific formatting (dates, numbers, etc.)
- Verify consistency of terminology across languages

### 4. Cross-Language Test Execution

- Run the same test scenarios across all supported languages
- Compare results across languages for consistency
- Identify language-specific issues or differences

## Test Data Management

### 1. Test Data Organization

- Organize test data by language, intent, and scenario
- Use consistent naming conventions for test data files
- Document test data structure and usage

### 2. Test Data Generation

- Implement utilities for generating test data
- Support generation of language-specific test data
- Include edge cases and boundary conditions

### 3. Test Data Versioning

- Version control test data alongside code
- Track changes to test data over time
- Maintain compatibility between test data and code

## Test Maintenance

### 1. Test Code Organization

- Use modular, reusable test components
- Separate test logic from test data
- Document test purpose and requirements

### 2. Test Refactoring

- Regularly review and refactor test code
- Eliminate duplication and improve reusability
- Update tests to reflect changes in requirements

### 3. Test Documentation

- Document test coverage and gaps
- Maintain test execution instructions
- Document test data requirements and usage

## Implementation Plan

### Phase 1: Framework Setup (Weeks 1-2)

1. Set up basic test framework structure
2. Implement core test utilities and fixtures
3. Create initial test data structure
4. Set up CI/CD integration

### Phase 2: Basic Test Implementation (Weeks 3-4)

1. Implement intent recognition tests
2. Implement entity extraction tests
3. Implement command routing tests
4. Set up basic reporting and monitoring

### Phase 3: Comprehensive Test Coverage (Weeks 5-6)

1. Implement WhatsApp integration tests
2. Implement API integration tests
3. Implement end-to-end tests
4. Enhance reporting and monitoring

### Phase 4: Performance and Scalability (Weeks 7-8)

1. Implement performance tests
2. Set up parallel test execution
3. Optimize test execution time
4. Implement advanced reporting and monitoring

## Conclusion

This test automation framework design provides a comprehensive approach to automated testing of the multilingual NLP command system. By implementing this framework, we can ensure thorough testing of all system components, improve test efficiency and reliability, and support continuous testing in the CI/CD pipeline.

The modular, extensible architecture allows for easy addition of new test cases and support for additional languages in the future. The focus on reusability and maintainability ensures that the framework can evolve alongside the system and continue to provide value over time.

## Appendices

### Appendix A: Sample Test Data

#### A.1: English Commands Test Data

```json
{
  "intent": "get_orders",
  "language": "english",
  "variations": [
    {
      "text": "show my orders",
      "entities": {},
      "expected_intent_confidence": 0.95
    },
    {
      "text": "show orders from last week",
      "entities": {"time_period": "last_week"},
      "expected_intent_confidence": 0.92
    },
    {
      "text": "show pending orders",
      "entities": {"status": "pending"},
      "expected_intent_confidence": 0.90
    },
    {
      "text": "show completed orders from yesterday",
      "entities": {"status": "completed", "time_period": "yesterday"},
      "expected_intent_confidence": 0.88
    },
    {
      "text": "what are my recent orders",
      "entities": {"time_period": "recent"},
      "expected_intent_confidence": 0.85
    }
  ]
}
```

#### A.2: Hindi Commands Test Data

```json
{
  "intent": "get_orders",
  "language": "hindi",
  "variations": [
    {
      "text": "मेरे ऑर्डर दिखाओ",
      "entities": {},
      "expected_intent_confidence": 0.92
    },
    {
      "text": "पिछले हफ्ते के ऑर्डर दिखाओ",
      "entities": {"time_period": "last_week"},
      "expected_intent_confidence": 0.90
    },
    {
      "text": "लंबित ऑर्डर दिखाओ",
      "entities": {"status": "pending"},
      "expected_intent_confidence": 0.88
    },
    {
      "text": "कल के पूरे हुए ऑर्डर दिखाओ",
      "entities": {"status": "completed", "time_period": "yesterday"},
      "expected_intent_confidence": 0.85
    },
    {
      "text": "मेरे हाल के ऑर्डर क्या हैं",
      "entities": {"time_period": "recent"},
      "expected_intent_confidence": 0.82
    }
  ]
}
```

#### A.3: API Mock Responses

```json
{
  "endpoint": "orders",
  "responses": {
    "success": {
      "status": 200,
      "body": {
        "orders": [
          {
            "id": "ORD12345",
            "date": "2023-05-01T10:30:00Z",
            "status": "completed",
            "total": 1500.00,
            "items": 3
          },
          {
            "id": "ORD12346",
            "date": "2023-05-02T14:45:00Z",
            "status": "pending",
            "total": 2500.00,
            "items": 5
          },
          {
            "id": "ORD12347",
            "date": "2023-05-03T09:15:00Z",
            "status": "processing",
            "total": 1800.00,
            "items": 4
          }
        ],
        "total_count": 3
      }
    },
    "empty": {
      "status": 200,
      "body": {
        "orders": [],
        "total_count": 0
      }
    },
    "error": {
      "status": 500,
      "body": {
        "error": "Internal server error",
        "message": "Unable to retrieve orders"
      }
    }
  }
}
```

### Appendix B: Test Configuration Examples

#### B.1: Environment Configuration

```python
# config/test_config.py
class TestConfig:
    """Test configuration settings."""
    
    # API configuration
    API_BASE_URL = "http://localhost:8000/api"
    API_TIMEOUT = 5  # seconds
    
    # WhatsApp configuration
    WHATSAPP_API_URL = "http://localhost:8001/api/whatsapp"
    WHATSAPP_TIMEOUT = 10  # seconds
    
    # Test data configuration
    TEST_DATA_DIR = "tests/test_data"
    
    # Reporting configuration
    REPORT_DIR = "reports"
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FILE = "test_execution.log"
    
    # Performance test configuration
    PERFORMANCE_TEST_DURATION = 60  # seconds
    PERFORMANCE_TEST_USERS = 10
    PERFORMANCE_TEST_SPAWN_RATE = 1  # users per second
```

#### B.2: Pytest Configuration

```ini
# pytest.ini
[pytest]
markers =
    english: Tests for English language
    hindi: Tests for Hindi language
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    slow: Tests that take a long time to run

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = -v --strict-markers

log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

### Appendix C: Test Execution Examples

#### C.1: Running Tests with Different Configurations

```bash
# Run tests with specific configuration
pytest --config=config/test_config.py

# Run tests with specific environment
ENV=staging pytest

# Run tests with specific language
pytest -m "english"

# Run tests with specific intent
pytest -k "get_orders"

# Run tests with specific test data
TEST_DATA_DIR=tests/test_data/custom pytest
```

#### C.2: Running Performance Tests

```bash
# Run Locust performance tests
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Run Locust in headless mode
locust -f tests/performance/locustfile.py --host=http://localhost:8000 --users=10 --spawn-rate=1 --run-time=60s --headless
```