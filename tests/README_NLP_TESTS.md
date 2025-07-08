# Multilingual NLP Testing Framework

## Overview

This directory contains test cases for validating the multilingual Natural Language Processing (NLP) capabilities of the OneTappe chatbot. The tests cover language detection, intent recognition, entity extraction, and response generation in English, Hindi, and mixed language inputs.

## Test Components

### 1. Multilingual Parser Tests

The `test_multilingual_parser.py` file contains tests for the enhanced multilingual parser, including:

- English command parsing
- Hindi command parsing
- Mixed language command parsing
- Romanized Hindi (Hinglish) command parsing
- Response formatting in different languages
- Error handling for invalid commands

### 2. Language Detection Tests

The `test_language_detection.py` file contains tests for the improved language detection module, including:

- Basic language detection
- Language detection with confidence scores
- Detailed mixed language detection
- Handling of mixed language input
- Edge cases for language detection

### 3. Mixed Entity Extraction Tests

The `test_mixed_entity_extraction.py` file contains tests for the mixed entity extraction module, including:

- Extraction of date ranges from mixed language text
- Parsing of mixed language date strings
- Extraction of product details from mixed language text
- Normalization of mixed language commands
- Edge cases for mixed entity extraction

### 4. Test Runner

The `run_nlp_tests.py` script runs all the test cases and generates a comprehensive test report, including:

- Summary of test results
- Details of any failures or errors
- Execution time statistics

## Running the Tests

### Running All Tests

To run all the NLP tests and generate a report:

```bash
python run_nlp_tests.py
```

This will execute all the test cases and save a markdown report in the `reports` directory.

### Running Individual Test Files

To run a specific test file:

```bash
python test_multilingual_parser.py
python test_language_detection.py
python test_mixed_entity_extraction.py
```

### Running Specific Test Cases

To run a specific test case:

```bash
python -m unittest test_multilingual_parser.TestMultilingualParser.test_english_command_parsing
```

## Test Reports

Test reports are generated in markdown format and saved in the `reports` directory. Each report includes:

- Summary of test results (total tests, passed, failed, errors, skipped)
- Details of any failures or errors
- Execution time statistics

## Adding New Tests

To add new tests:

1. Add new test methods to the existing test classes, or
2. Create a new test file with a new test class
3. If creating a new test file, add it to the test suite in `run_nlp_tests.py`

## Integration with CI/CD

The test runner returns a non-zero exit code if any tests fail, making it suitable for integration with CI/CD pipelines.

## Dependencies

The tests depend on the following modules:

- `unittest`: Python's built-in testing framework
- `OneTappeProject.nlp`: The NLP modules being tested

## Best Practices

1. Keep test methods focused on testing a single functionality
2. Use descriptive test method names
3. Include docstrings explaining what each test is verifying
4. Use assertions to verify expected behavior
5. Handle edge cases and error conditions
6. Keep tests independent of each other