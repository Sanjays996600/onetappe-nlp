# Test Prioritization Framework for OneTappe API

## Overview

The Test Prioritization Framework is designed to optimize test execution by running the most important tests first based on risk assessment and efficiency metrics. This framework helps QA teams focus their testing efforts on the most critical parts of the application, especially when working with time constraints.

## Integration with Test Runner

The test prioritization functionality has been integrated with the main test runner (`run_all_tests.py`), allowing you to run prioritized tests as part of your regular testing workflow.

## Key Components

1. **Test Prioritizer (`prioritize_test_cases.py`)**: Analyzes test cases and assigns priority levels based on risk and efficiency metrics.

2. **Prioritized Test Runner (`run_prioritized_tests.py`)**: Executes tests based on their priority levels and within a specified time budget.

3. **Test Runner Integration (`run_all_tests.py`)**: Provides command-line options to run prioritized tests alongside other test types.

## How to Use

### Basic Usage

To run prioritized tests using the main test runner:

```bash
python run_all_tests.py --prioritized
```

This will run all tests based on their priority levels, starting with the most critical ones.

### Advanced Options

You can customize the prioritized test run with the following options:

```bash
python run_all_tests.py --prioritized --prioritized-time-budget 300 --prioritized-categories "product,authentication" --prioritized-levels "P1 - Critical,P2 - High"
```

Where:
- `--prioritized-time-budget`: Maximum time in seconds to spend running tests (e.g., 300 for 5 minutes)
- `--prioritized-categories`: Comma-separated list of test categories to include (e.g., "product,authentication,seller_dashboard")
- `--prioritized-levels`: Comma-separated list of priority levels to include (e.g., "P1 - Critical,P2 - High")

### Running with All Tests

To run prioritized tests along with all other test types:

```bash
python run_all_tests.py --all
```

The `--all` flag now includes prioritized tests in addition to functional, performance, security, load tests, and report generation.

## Priority Levels

Tests are categorized into the following priority levels:

1. **P1 - Critical**: Tests that verify core functionality and have high business impact. Failures in these tests would severely impact the application.

2. **P2 - High**: Tests that verify important functionality but are not critical for the application to function.

3. **P3 - Medium**: Tests that verify secondary functionality or edge cases.

4. **P4 - Low**: Tests that verify minor functionality or are less likely to fail.

## Test Categories

Tests are organized into the following categories:

1. **Product**: Tests related to product listing, details, search, and filtering.

2. **Authentication**: Tests related to user registration, login, and authorization.

3. **Seller Dashboard**: Tests related to seller functionality, including product management and order processing.

4. **Performance**: Tests that measure response times and system performance under various conditions.

5. **Security**: Tests that verify the application's security measures and identify vulnerabilities.

## Reports

After running prioritized tests, a detailed report is generated at `backend/testing/prioritized_test_report.md`. This report includes:

- Summary of test results by outcome (pass, fail, error, timeout, skip)
- Results grouped by test category
- Results grouped by priority level
- Recommendations based on test results
- List of the slowest tests

## Test History

The framework maintains a history of test executions to track patterns over time. This history is used to adjust test priorities based on:

- Recent failures
- Execution frequency
- Historical stability

## Best Practices

1. **Regular Full Test Runs**: While prioritized testing is efficient for daily development, schedule regular full test runs to ensure complete coverage.

2. **Update Test Metadata**: Keep test metadata (business impact, failure probability, etc.) up to date to ensure accurate prioritization.

3. **Review Priority Assignments**: Periodically review and adjust priority assignments based on changing business requirements and application evolution.

4. **Balance Time Budget**: Set a reasonable time budget that allows for sufficient coverage while meeting your development cycle needs.

## Troubleshooting

### Common Issues

1. **Missing Test History**: If test history is missing, the framework will use default values based on test metadata.

2. **Incorrect Priority Assignments**: If tests seem incorrectly prioritized, check the metadata in `prioritize_test_cases.py` or update the test history.

3. **Time Budget Too Short**: If important tests are being skipped, increase the time budget or adjust the priority levels to include.

## Future Enhancements

1. **Machine Learning Integration**: Implement ML algorithms to predict test failures based on code changes.

2. **CI/CD Integration**: Enhance integration with CI/CD pipelines for automated prioritized testing.

3. **Dynamic Time Allocation**: Dynamically adjust time allocation based on test importance and historical execution times.

4. **Test Dependency Analysis**: Incorporate test dependencies to ensure prerequisite tests are run before dependent tests.

5. **Visual Reporting Dashboard**: Develop a visual dashboard for test results and prioritization metrics.