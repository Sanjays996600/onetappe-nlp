# Automated Testing Plan for NLP Command System

## Overview
This document outlines a comprehensive automated testing strategy for the multilingual NLP command system. The plan focuses on ensuring reliability, accuracy, and performance across all supported intents and languages.

## Goals
- Ensure consistent intent recognition across all supported languages
- Verify accurate entity extraction (limits, time periods, product names, etc.)
- Validate proper command routing and API integration
- Test error handling and edge cases
- Measure and optimize system performance
- Ensure seamless WhatsApp integration

## Testing Framework

### Core Components
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete user flows
- **Performance Tests**: Measure response times and throughput
- **Continuous Integration**: Automate test execution on code changes

### Tools and Libraries
- **pytest**: Primary testing framework
- **unittest.mock**: For mocking dependencies
- **pytest-cov**: For measuring code coverage
- **locust**: For load and performance testing
- **pytest-benchmark**: For performance benchmarking
- **pytest-xdist**: For parallel test execution

## Test Categories

### 1. Intent Recognition Tests

#### Approach
- Create a comprehensive test dataset with varied phrasings for each intent
- Test both English and Hindi commands with different sentence structures
- Include edge cases with mixed languages and ambiguous commands
- Measure confidence scores and verify threshold settings

#### Implementation Example
```python
@pytest.mark.parametrize("command,expected_intent,expected_language", [
    ("show top 5 products", "get_top_products", "en"),
    ("टॉप 5 प्रोडक्ट्स दिखाओ", "get_top_products", "hi"),
    ("what are my best sellers", "get_top_products", "en"),
    ("मेरे बेस्ट सेलर क्या हैं", "get_top_products", "hi"),
    # More test cases for other intents
])
def test_intent_recognition(command, expected_intent, expected_language):
    result = parse_multilingual_command(command)
    assert result["intent"] == expected_intent
    assert result["language"] == expected_language
```

### 2. Entity Extraction Tests

#### Approach
- Test extraction of various entity types (numbers, dates, product names, etc.)
- Verify handling of different formats and variations
- Test edge cases (very large numbers, unusual date formats)
- Verify defaults when entities are not specified

#### Implementation Example
```python
@pytest.mark.parametrize("command,expected_entities", [
    ("show top 5 products this month", {"limit": 5, "time_period": "this month"}),
    ("इस हफ्ते के टॉप 10 प्रोडक्ट्स दिखाओ", {"limit": 10, "time_period": "this week"}),
    ("search for rice", {"product_name": "rice"}),
    ("चावल के बारे में जानकारी दो", {"product_name": "चावल"}),
    # More test cases
])
def test_entity_extraction(command, expected_entities):
    result = parse_multilingual_command(command)
    for key, value in expected_entities.items():
        assert result["entities"].get(key) == value
```

### 3. Command Routing Tests

#### Approach
- Mock API responses for each intent
- Verify correct API endpoints are called with appropriate parameters
- Test response formatting and localization
- Verify error handling for API failures

#### Implementation Example
```python
def test_command_routing():
    parsed_result = {
        "intent": "get_top_products",
        "language": "en",
        "entities": {"limit": 5, "time_period": "this month"}
    }
    
    mock_api_response = {
        "success": True,
        "products": [
            {"name": "Rice", "sales": 500, "revenue": 25000},
            {"name": "Sugar", "sales": 300, "revenue": 15000}
        ]
    }
    
    with patch("nlp.command_router.make_api_request") as mock_api:
        mock_api.return_value = mock_api_response
        response = route_command(parsed_result)
        
        # Verify API was called correctly
        mock_api.assert_called_once()
        args, kwargs = mock_api.call_args
        assert kwargs.get("endpoint") == "get_top_products"
        assert kwargs.get("params").get("limit") == 5
        
        # Verify response formatting
        assert "Top 5 products" in response
        assert "Rice" in response
        assert "500" in response
```

### 4. WhatsApp Integration Tests

#### Approach
- Mock WhatsApp gateway for sending/receiving messages
- Test session management and conversation flow
- Verify proper handling of Unicode and special characters
- Test error recovery and fallback mechanisms

#### Implementation Example
```python
def test_whatsapp_integration():
    gateway = MockWhatsAppGateway()
    handler = WhatsAppIntegrationHandler(gateway)
    
    # Test English command
    handler.process_message("user123", "show inventory")
    assert gateway.last_message_sent == "user123"
    assert "Inventory" in gateway.last_message_content
    
    # Test Hindi command
    handler.process_message("user456", "इन्वेंटरी दिखाओ")
    assert gateway.last_message_sent == "user456"
    assert "इन्वेंटरी" in gateway.last_message_content
    
    # Test conversation flow
    handler.process_message("user789", "show top products")
    assert "Top products" in gateway.last_message_content
    handler.process_message("user789", "show more details")
    assert "More details" in gateway.last_message_content
```

### 5. Performance Tests

#### Approach
- Measure response times for different intents and languages
- Test system under various load conditions
- Identify bottlenecks and optimization opportunities
- Set performance baselines and monitor for regressions

#### Implementation Example
```python
@pytest.mark.benchmark
def test_performance_english_commands(benchmark):
    commands = [
        "show inventory",
        "show top 5 products",
        "search for rice",
        "show low stock items",
        "show customer data"
    ]
    
    def run_commands():
        results = []
        for cmd in commands:
            parsed = parse_multilingual_command(cmd)
            results.append(parsed)
        return results
    
    results = benchmark(run_commands)
    assert len(results) == len(commands)

@pytest.mark.benchmark
def test_performance_hindi_commands(benchmark):
    commands = [
        "इन्वेंटरी दिखाओ",
        "टॉप 5 प्रोडक्ट्स दिखाओ",
        "चावल के बारे में जानकारी दो",
        "कम स्टॉक वाले आइटम दिखाओ",
        "ग्राहक डेटा दिखाओ"
    ]
    
    def run_commands():
        results = []
        for cmd in commands:
            parsed = parse_multilingual_command(cmd)
            results.append(parsed)
        return results
    
    results = benchmark(run_commands)
    assert len(results) == len(commands)
```

### 6. Error Handling Tests

#### Approach
- Test system response to invalid commands
- Verify appropriate error messages in all supported languages
- Test recovery from API failures
- Verify graceful handling of malformed inputs

#### Implementation Example
```python
@pytest.mark.parametrize("command,language", [
    ("gibberish text", "en"),
    ("अजीब टेक्स्ट", "hi"),
    ("123456", "en"),
    ("!@#$%^", "en")
])
def test_invalid_command_handling(command, language):
    result = parse_multilingual_command(command)
    assert result["intent"] == "unknown"
    assert result["language"] == language
    
    response = route_command(result)
    if language == "en":
        assert "I couldn't understand" in response or "I'm not sure" in response
    else:
        assert "मैं समझ नहीं पाया" in response or "मुझे यकीन नहीं है" in response

def test_api_failure_handling():
    parsed_result = {"intent": "get_inventory", "language": "en"}
    
    with patch("nlp.command_router.make_api_request") as mock_api:
        mock_api.return_value = {"success": False, "error": "API Error"}
        response = route_command(parsed_result)
        assert "error" in response.lower()
        assert "inventory" in response.lower()
```

## Continuous Integration Setup

### Pipeline Configuration
1. **Linting and Static Analysis**
   - Run flake8 and mypy to catch syntax and type errors

2. **Unit Tests**
   - Run pytest with coverage reporting
   - Fail if coverage drops below 80%

3. **Integration Tests**
   - Run integration test suite with mocked dependencies

4. **Performance Tests**
   - Run benchmark tests and compare with baseline
   - Alert on significant performance regressions

### Example CI Configuration (GitHub Actions)
```yaml
name: NLP System Tests

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
        pip install flake8 pytest pytest-cov pytest-benchmark
        pip install -r requirements.txt
    - name: Lint with flake8
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Test with pytest
      run: pytest --cov=nlp --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
    - name: Run benchmark tests
      run: pytest nlp/tests/test_performance.py --benchmark-json=output.json
    - name: Compare benchmarks
      uses: benchmark-action/github-action-benchmark@v1
      with:
        tool: 'pytest'
        output-file-path: output.json
```

## Test Data Management

### Training and Test Data Separation
- Maintain separate datasets for training NLP models and testing
- Ensure test data covers all intents, entities, and languages
- Include edge cases and challenging examples

### Test Data Versioning
- Version control test datasets alongside code
- Document changes to test data
- Maintain a growing corpus of test cases

## Reporting and Monitoring

### Test Reports
- Generate detailed test reports with pass/fail statistics
- Track coverage metrics over time
- Visualize performance benchmarks

### Monitoring
- Set up monitoring for production system
- Track intent recognition accuracy
- Monitor response times and error rates
- Alert on anomalies

## Implementation Schedule

### Phase 1: Core Test Framework
- Set up pytest infrastructure
- Implement basic unit tests for all intents
- Configure CI pipeline

### Phase 2: Comprehensive Test Suite
- Expand test coverage for all edge cases
- Implement integration tests
- Add performance benchmarks

### Phase 3: Automation and Monitoring
- Automate regression testing
- Set up monitoring and alerting
- Implement continuous performance testing

## Conclusion
This automated testing plan provides a comprehensive approach to ensuring the quality and reliability of the NLP command system. By implementing these testing strategies, we can confidently deliver a robust multilingual system that meets user expectations across all supported languages and use cases.