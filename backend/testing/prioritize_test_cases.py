#!/usr/bin/env python3
"""
Test Case Prioritization for OneTappe API

This script analyzes and prioritizes test cases based on risk, importance, and other factors.
It helps QA teams focus on the most critical tests first and optimize test execution.

Prioritization factors include:
- Business impact
- Failure probability
- Test execution time
- Code coverage
- Recent failures
- Feature usage
"""

import os
import sys
import json
import csv
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test_prioritization.log")
    ]
)
logger = logging.getLogger("test_prioritization")

# Constants
BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_FILE = BASE_DIR / "test_cases.json"
TEST_HISTORY_FILE = BASE_DIR / "test_history.json"
PRIORITIZED_TESTS_FILE = BASE_DIR / "prioritized_tests.json"
PRIORITIZED_TESTS_CSV = BASE_DIR / "prioritized_tests.csv"
PRIORITIZED_TESTS_MD = BASE_DIR / "prioritized_tests.md"

# Risk levels
RISK_LEVELS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1
}

# Test categories
TEST_CATEGORIES = [
    "product_api",
    "authentication",
    "seller_dashboard",
    "order_management",
    "user_management",
    "search_functionality",
    "payment_processing",
    "security",
    "performance"
]

# Sample test cases (for demonstration)
SAMPLE_TEST_CASES = [
    {
        "id": "PROD-001",
        "name": "Add product with valid data",
        "category": "product_api",
        "description": "Test adding a product with all required fields and valid data",
        "business_impact": "high",
        "failure_probability": "medium",
        "execution_time": 2.5,  # seconds
        "code_coverage": 0.8,  # 0.0 to 1.0
        "dependencies": [],
        "automated": True
    },
    {
        "id": "PROD-002",
        "name": "Add product without seller_id",
        "category": "product_api",
        "description": "Test adding a product without seller_id (should fail with appropriate error)",
        "business_impact": "high",
        "failure_probability": "high",
        "execution_time": 2.0,
        "code_coverage": 0.6,
        "dependencies": [],
        "automated": True
    },
    {
        "id": "PROD-003",
        "name": "Get product by ID",
        "category": "product_api",
        "description": "Test retrieving a product by its ID",
        "business_impact": "high",
        "failure_probability": "low",
        "execution_time": 1.5,
        "code_coverage": 0.5,
        "dependencies": ["PROD-001"],
        "automated": True
    },
    {
        "id": "PROD-004",
        "name": "Update product",
        "category": "product_api",
        "description": "Test updating a product's information",
        "business_impact": "medium",
        "failure_probability": "medium",
        "execution_time": 2.0,
        "code_coverage": 0.7,
        "dependencies": ["PROD-001"],
        "automated": True
    },
    {
        "id": "PROD-005",
        "name": "Delete product",
        "category": "product_api",
        "description": "Test deleting a product",
        "business_impact": "medium",
        "failure_probability": "low",
        "execution_time": 1.5,
        "code_coverage": 0.6,
        "dependencies": ["PROD-001"],
        "automated": True
    },
    {
        "id": "AUTH-001",
        "name": "User login with valid credentials",
        "category": "authentication",
        "description": "Test user login with valid username and password",
        "business_impact": "critical",
        "failure_probability": "low",
        "execution_time": 1.0,
        "code_coverage": 0.9,
        "dependencies": [],
        "automated": True
    },
    {
        "id": "AUTH-002",
        "name": "User login with invalid credentials",
        "category": "authentication",
        "description": "Test user login with invalid username or password",
        "business_impact": "high",
        "failure_probability": "low",
        "execution_time": 1.0,
        "code_coverage": 0.7,
        "dependencies": [],
        "automated": True
    },
    {
        "id": "AUTH-003",
        "name": "Token validation",
        "category": "authentication",
        "description": "Test validating authentication tokens",
        "business_impact": "critical",
        "failure_probability": "medium",
        "execution_time": 1.5,
        "code_coverage": 0.8,
        "dependencies": ["AUTH-001"],
        "automated": True
    },
    {
        "id": "SELLER-001",
        "name": "Seller dashboard access",
        "category": "seller_dashboard",
        "description": "Test seller access to their dashboard",
        "business_impact": "high",
        "failure_probability": "medium",
        "execution_time": 2.0,
        "code_coverage": 0.7,
        "dependencies": ["AUTH-001"],
        "automated": True
    },
    {
        "id": "SELLER-002",
        "name": "Seller product management",
        "category": "seller_dashboard",
        "description": "Test seller's ability to manage their products",
        "business_impact": "high",
        "failure_probability": "medium",
        "execution_time": 3.0,
        "code_coverage": 0.8,
        "dependencies": ["SELLER-001", "PROD-001"],
        "automated": True
    },
    {
        "id": "SELLER-003",
        "name": "Seller order management",
        "category": "seller_dashboard",
        "description": "Test seller's ability to manage their orders",
        "business_impact": "critical",
        "failure_probability": "high",
        "execution_time": 3.5,
        "code_coverage": 0.9,
        "dependencies": ["SELLER-001"],
        "automated": True
    },
    {
        "id": "PERF-001",
        "name": "Product API response time",
        "category": "performance",
        "description": "Test response time of product API endpoints",
        "business_impact": "medium",
        "failure_probability": "medium",
        "execution_time": 10.0,
        "code_coverage": 0.5,
        "dependencies": ["PROD-001", "PROD-003"],
        "automated": True
    },
    {
        "id": "PERF-002",
        "name": "Authentication API response time",
        "category": "performance",
        "description": "Test response time of authentication API endpoints",
        "business_impact": "high",
        "failure_probability": "medium",
        "execution_time": 8.0,
        "code_coverage": 0.6,
        "dependencies": ["AUTH-001"],
        "automated": True
    },
    {
        "id": "SEC-001",
        "name": "SQL injection prevention",
        "category": "security",
        "description": "Test prevention of SQL injection attacks",
        "business_impact": "critical",
        "failure_probability": "medium",
        "execution_time": 5.0,
        "code_coverage": 0.7,
        "dependencies": [],
        "automated": True
    },
    {
        "id": "SEC-002",
        "name": "XSS prevention",
        "category": "security",
        "description": "Test prevention of cross-site scripting attacks",
        "business_impact": "critical",
        "failure_probability": "medium",
        "execution_time": 4.5,
        "code_coverage": 0.7,
        "dependencies": [],
        "automated": True
    }
]

# Sample test history (for demonstration)
SAMPLE_TEST_HISTORY = {
    "PROD-001": {
        "last_execution": "2023-06-15T10:30:00",
        "last_result": "pass",
        "execution_count": 15,
        "failure_count": 0,
        "recent_results": ["pass", "pass", "pass", "pass", "pass"]
    },
    "PROD-002": {
        "last_execution": "2023-06-15T10:32:00",
        "last_result": "fail",
        "execution_count": 12,
        "failure_count": 8,
        "recent_results": ["fail", "fail", "pass", "fail", "fail"]
    },
    "PROD-003": {
        "last_execution": "2023-06-15T10:34:00",
        "last_result": "pass",
        "execution_count": 15,
        "failure_count": 1,
        "recent_results": ["pass", "pass", "pass", "pass", "fail"]
    },
    "PROD-004": {
        "last_execution": "2023-06-15T10:36:00",
        "last_result": "pass",
        "execution_count": 10,
        "failure_count": 2,
        "recent_results": ["pass", "pass", "fail", "pass", "pass"]
    },
    "PROD-005": {
        "last_execution": "2023-06-15T10:38:00",
        "last_result": "pass",
        "execution_count": 10,
        "failure_count": 0,
        "recent_results": ["pass", "pass", "pass", "pass", "pass"]
    },
    "AUTH-001": {
        "last_execution": "2023-06-15T10:40:00",
        "last_result": "pass",
        "execution_count": 20,
        "failure_count": 0,
        "recent_results": ["pass", "pass", "pass", "pass", "pass"]
    },
    "AUTH-002": {
        "last_execution": "2023-06-15T10:42:00",
        "last_result": "pass",
        "execution_count": 18,
        "failure_count": 0,
        "recent_results": ["pass", "pass", "pass", "pass", "pass"]
    },
    "AUTH-003": {
        "last_execution": "2023-06-15T10:44:00",
        "last_result": "fail",
        "execution_count": 15,
        "failure_count": 3,
        "recent_results": ["fail", "pass", "pass", "pass", "fail"]
    },
    "SELLER-001": {
        "last_execution": "2023-06-15T10:46:00",
        "last_result": "pass",
        "execution_count": 12,
        "failure_count": 1,
        "recent_results": ["pass", "pass", "pass", "pass", "fail"]
    },
    "SELLER-002": {
        "last_execution": "2023-06-15T10:48:00",
        "last_result": "pass",
        "execution_count": 10,
        "failure_count": 2,
        "recent_results": ["pass", "fail", "pass", "pass", "pass"]
    },
    "SELLER-003": {
        "last_execution": "2023-06-15T10:50:00",
        "last_result": "fail",
        "execution_count": 8,
        "failure_count": 3,
        "recent_results": ["fail", "pass", "fail", "pass", "pass"]
    },
    "PERF-001": {
        "last_execution": "2023-06-15T11:00:00",
        "last_result": "pass",
        "execution_count": 5,
        "failure_count": 1,
        "recent_results": ["pass", "pass", "fail", "pass", "pass"]
    },
    "PERF-002": {
        "last_execution": "2023-06-15T11:10:00",
        "last_result": "pass",
        "execution_count": 5,
        "failure_count": 2,
        "recent_results": ["pass", "fail", "pass", "fail", "pass"]
    },
    "SEC-001": {
        "last_execution": "2023-06-15T11:20:00",
        "last_result": "pass",
        "execution_count": 8,
        "failure_count": 0,
        "recent_results": ["pass", "pass", "pass", "pass", "pass"]
    },
    "SEC-002": {
        "last_execution": "2023-06-15T11:30:00",
        "last_result": "pass",
        "execution_count": 8,
        "failure_count": 1,
        "recent_results": ["pass", "pass", "pass", "fail", "pass"]
    }
}


class TestPrioritizer:
    """Prioritizes test cases based on various factors."""
    
    def __init__(self, test_cases=None, test_history=None):
        """Initialize with test cases and history."""
        self.test_cases = test_cases or []
        self.test_history = test_history or {}
        self.prioritized_tests = []
    
    def load_test_cases(self, file_path=TEST_CASES_FILE):
        """Load test cases from a JSON file."""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.test_cases = json.load(f)
                logger.info(f"Loaded {len(self.test_cases)} test cases from {file_path}")
                return True
            else:
                logger.warning(f"Test cases file not found: {file_path}")
                logger.info("Using sample test cases for demonstration")
                self.test_cases = SAMPLE_TEST_CASES
                return True
        except Exception as e:
            logger.error(f"Error loading test cases: {e}")
            return False
    
    def load_test_history(self, file_path=TEST_HISTORY_FILE):
        """Load test execution history from a JSON file."""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.test_history = json.load(f)
                logger.info(f"Loaded test history for {len(self.test_history)} tests from {file_path}")
                return True
            else:
                logger.warning(f"Test history file not found: {file_path}")
                logger.info("Using sample test history for demonstration")
                self.test_history = SAMPLE_TEST_HISTORY
                return True
        except Exception as e:
            logger.error(f"Error loading test history: {e}")
            return False
    
    def calculate_risk_score(self, test_case):
        """Calculate risk score for a test case."""
        # Business impact score (0-4)
        business_impact = RISK_LEVELS.get(test_case.get("business_impact", "low"), 1)
        
        # Failure probability score (0-4)
        failure_probability = RISK_LEVELS.get(test_case.get("failure_probability", "low"), 1)
        
        # Recent failures score (0-3)
        recent_failures = 0
        test_id = test_case.get("id")
        if test_id in self.test_history:
            history = self.test_history[test_id]
            recent_results = history.get("recent_results", [])
            recent_failures = sum(1 for result in recent_results if result == "fail")
        
        # Last result score (0 or 2)
        last_result_score = 0
        if test_id in self.test_history and self.test_history[test_id].get("last_result") == "fail":
            last_result_score = 2
        
        # Calculate final risk score (0-13)
        risk_score = business_impact + failure_probability + recent_failures + last_result_score
        
        return risk_score
    
    def calculate_efficiency_score(self, test_case):
        """Calculate efficiency score for a test case."""
        # Code coverage score (0-10)
        code_coverage = test_case.get("code_coverage", 0) * 10
        
        # Execution time score (0-5)
        execution_time = test_case.get("execution_time", 1)
        execution_time_score = max(0, 5 - execution_time / 2)  # Lower time is better
        
        # Automation score (0 or 3)
        automation_score = 3 if test_case.get("automated", False) else 0
        
        # Calculate final efficiency score (0-18)
        efficiency_score = code_coverage + execution_time_score + automation_score
        
        return efficiency_score
    
    def prioritize_tests(self):
        """Prioritize test cases based on risk and efficiency."""
        logger.info("Prioritizing test cases...")
        
        # Calculate scores for each test case
        scored_tests = []
        for test_case in self.test_cases:
            risk_score = self.calculate_risk_score(test_case)
            efficiency_score = self.calculate_efficiency_score(test_case)
            
            # Calculate priority score (risk has higher weight)
            priority_score = (risk_score * 2) + efficiency_score
            
            scored_test = test_case.copy()
            scored_test["risk_score"] = risk_score
            scored_test["efficiency_score"] = efficiency_score
            scored_test["priority_score"] = priority_score
            
            # Add test history if available
            test_id = test_case.get("id")
            if test_id in self.test_history:
                scored_test["history"] = self.test_history[test_id]
            
            scored_tests.append(scored_test)
        
        # Sort by priority score (descending)
        self.prioritized_tests = sorted(scored_tests, key=lambda x: x["priority_score"], reverse=True)
        
        # Assign priority levels
        for i, test in enumerate(self.prioritized_tests):
            if i < len(self.prioritized_tests) * 0.2:  # Top 20%
                test["priority_level"] = "P1 - Critical"
            elif i < len(self.prioritized_tests) * 0.5:  # Next 30%
                test["priority_level"] = "P2 - High"
            elif i < len(self.prioritized_tests) * 0.8:  # Next 30%
                test["priority_level"] = "P3 - Medium"
            else:  # Bottom 20%
                test["priority_level"] = "P4 - Low"
        
        logger.info(f"Prioritized {len(self.prioritized_tests)} test cases")
        return self.prioritized_tests
    
    def save_prioritized_tests(self, file_path=PRIORITIZED_TESTS_FILE):
        """Save prioritized tests to a JSON file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(self.prioritized_tests, f, indent=2)
            logger.info(f"Saved prioritized tests to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving prioritized tests: {e}")
            return False
    
    def export_to_csv(self, file_path=PRIORITIZED_TESTS_CSV):
        """Export prioritized tests to a CSV file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Priority", "ID", "Name", "Category", "Priority Level",
                    "Risk Score", "Efficiency Score", "Priority Score",
                    "Business Impact", "Failure Probability", "Last Result",
                    "Execution Time", "Code Coverage", "Automated"
                ])
                
                # Write test cases
                for i, test in enumerate(self.prioritized_tests, 1):
                    last_result = "N/A"
                    if "history" in test and "last_result" in test["history"]:
                        last_result = test["history"]["last_result"]
                    
                    writer.writerow([
                        i,
                        test.get("id", ""),
                        test.get("name", ""),
                        test.get("category", ""),
                        test.get("priority_level", ""),
                        test.get("risk_score", 0),
                        test.get("efficiency_score", 0),
                        test.get("priority_score", 0),
                        test.get("business_impact", ""),
                        test.get("failure_probability", ""),
                        last_result,
                        test.get("execution_time", 0),
                        test.get("code_coverage", 0),
                        "Yes" if test.get("automated", False) else "No"
                    ])
            
            logger.info(f"Exported prioritized tests to CSV: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def export_to_markdown(self, file_path=PRIORITIZED_TESTS_MD):
        """Export prioritized tests to a Markdown file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w") as f:
                f.write("# Prioritized Test Cases\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Summary
                f.write("## Summary\n\n")
                
                priority_counts = {
                    "P1 - Critical": 0,
                    "P2 - High": 0,
                    "P3 - Medium": 0,
                    "P4 - Low": 0
                }
                
                for test in self.prioritized_tests:
                    priority_level = test.get("priority_level", "")
                    if priority_level in priority_counts:
                        priority_counts[priority_level] += 1
                
                f.write("| Priority Level | Count | Percentage |\n")
                f.write("|---------------|-------|------------|\n")
                
                total_tests = len(self.prioritized_tests)
                for level, count in priority_counts.items():
                    percentage = (count / total_tests) * 100 if total_tests > 0 else 0
                    f.write(f"| {level} | {count} | {percentage:.1f}% |\n")
                
                f.write(f"| **Total** | **{total_tests}** | **100.0%** |\n\n")
                
                # Category breakdown
                f.write("## Category Breakdown\n\n")
                
                category_counts = {}
                for test in self.prioritized_tests:
                    category = test.get("category", "unknown")
                    if category not in category_counts:
                        category_counts[category] = 0
                    category_counts[category] += 1
                
                f.write("| Category | Count | Percentage |\n")
                f.write("|----------|-------|------------|\n")
                
                for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total_tests) * 100 if total_tests > 0 else 0
                    f.write(f"| {category} | {count} | {percentage:.1f}% |\n")
                
                f.write("\n")
                
                # Prioritized test cases
                f.write("## Prioritized Test Cases\n\n")
                
                # Group by priority level
                for level in ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"]:
                    level_tests = [test for test in self.prioritized_tests if test.get("priority_level") == level]
                    
                    if level_tests:
                        f.write(f"### {level}\n\n")
                        
                        f.write("| # | ID | Name | Category | Risk | Efficiency | Priority | Last Result |\n")
                        f.write("|---|----|----|----------|------|------------|----------|------------|\n")
                        
                        for i, test in enumerate(level_tests, 1):
                            last_result = "N/A"
                            if "history" in test and "last_result" in test["history"]:
                                last_result = test["history"]["last_result"]
                                if last_result == "pass":
                                    last_result = "✅ Pass"
                                elif last_result == "fail":
                                    last_result = "❌ Fail"
                            
                            f.write(f"| {i} | {test.get('id', '')} | {test.get('name', '')} | {test.get('category', '')} | {test.get('risk_score', 0)} | {test.get('efficiency_score', 0)} | {test.get('priority_score', 0)} | {last_result} |\n")
                        
                        f.write("\n")
                
                # Test details
                f.write("## Test Details\n\n")
                
                for test in self.prioritized_tests[:10]:  # Show details for top 10 tests
                    f.write(f"### {test.get('id', '')} - {test.get('name', '')}\n\n")
                    
                    f.write(f"**Priority Level:** {test.get('priority_level', '')}\n\n")
                    f.write(f"**Category:** {test.get('category', '')}\n\n")
                    f.write(f"**Description:** {test.get('description', '')}\n\n")
                    
                    f.write("**Scores:**\n")
                    f.write(f"- Risk Score: {test.get('risk_score', 0)}\n")
                    f.write(f"- Efficiency Score: {test.get('efficiency_score', 0)}\n")
                    f.write(f"- Priority Score: {test.get('priority_score', 0)}\n\n")
                    
                    f.write("**Factors:**\n")
                    f.write(f"- Business Impact: {test.get('business_impact', '')}\n")
                    f.write(f"- Failure Probability: {test.get('failure_probability', '')}\n")
                    f.write(f"- Execution Time: {test.get('execution_time', 0)} seconds\n")
                    f.write(f"- Code Coverage: {test.get('code_coverage', 0) * 100:.1f}%\n")
                    f.write(f"- Automated: {'Yes' if test.get('automated', False) else 'No'}\n\n")
                    
                    if "history" in test:
                        history = test["history"]
                        f.write("**Test History:**\n")
                        f.write(f"- Last Execution: {history.get('last_execution', 'N/A')}\n")
                        f.write(f"- Last Result: {history.get('last_result', 'N/A')}\n")
                        f.write(f"- Execution Count: {history.get('execution_count', 0)}\n")
                        f.write(f"- Failure Count: {history.get('failure_count', 0)}\n")
                        
                        recent_results = history.get("recent_results", [])
                        if recent_results:
                            f.write("- Recent Results: ")
                            for result in recent_results:
                                if result == "pass":
                                    f.write("✅ ")
                                else:
                                    f.write("❌ ")
                            f.write("\n")
                    
                    f.write("\n")
                
                # Recommendations
                f.write("## Recommendations\n\n")
                
                f.write("1. **Focus on P1 (Critical) tests first** - These tests have the highest risk and impact.\n")
                f.write("2. **Address failing tests** - Prioritize tests that have recently failed or have a high failure rate.\n")
                f.write("3. **Optimize test execution** - Consider running high-priority tests more frequently.\n")
                f.write("4. **Increase automation coverage** - Automate manual tests, especially those with high priority.\n")
                f.write("5. **Review test dependencies** - Ensure that dependent tests are executed in the correct order.\n")
            
            logger.info(f"Exported prioritized tests to Markdown: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to Markdown: {e}")
            return False
    
    def generate_test_suite(self, time_budget=60, category=None, priority_level=None):
        """Generate a test suite based on time budget and filters."""
        if not self.prioritized_tests:
            logger.warning("No prioritized tests available. Run prioritize_tests() first.")
            return []
        
        # Filter tests by category and priority level
        filtered_tests = self.prioritized_tests
        
        if category:
            filtered_tests = [test for test in filtered_tests if test.get("category") == category]
        
        if priority_level:
            filtered_tests = [test for test in filtered_tests if test.get("priority_level") == priority_level]
        
        # Sort by priority score (descending)
        sorted_tests = sorted(filtered_tests, key=lambda x: x.get("priority_score", 0), reverse=True)
        
        # Select tests that fit within the time budget
        selected_tests = []
        remaining_time = time_budget
        
        for test in sorted_tests:
            execution_time = test.get("execution_time", 0)
            
            if execution_time <= remaining_time:
                selected_tests.append(test)
                remaining_time -= execution_time
            
            if remaining_time <= 0:
                break
        
        logger.info(f"Generated test suite with {len(selected_tests)} tests (time budget: {time_budget} seconds)")
        return selected_tests


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Prioritize test cases for OneTappe API")
    parser.add_argument("--test-cases", type=str, default=TEST_CASES_FILE, help="Path to test cases JSON file")
    parser.add_argument("--test-history", type=str, default=TEST_HISTORY_FILE, help="Path to test history JSON file")
    parser.add_argument("--output-json", type=str, default=PRIORITIZED_TESTS_FILE, help="Path to output JSON file")
    parser.add_argument("--output-csv", type=str, default=PRIORITIZED_TESTS_CSV, help="Path to output CSV file")
    parser.add_argument("--output-md", type=str, default=PRIORITIZED_TESTS_MD, help="Path to output Markdown file")
    parser.add_argument("--generate-sample", action="store_true", help="Generate sample test cases and history files")
    args = parser.parse_args()
    
    # Generate sample files if requested
    if args.generate_sample:
        logger.info("Generating sample test cases and history files...")
        
        os.makedirs(os.path.dirname(TEST_CASES_FILE), exist_ok=True)
        with open(TEST_CASES_FILE, "w") as f:
            json.dump(SAMPLE_TEST_CASES, f, indent=2)
        logger.info(f"Generated sample test cases: {TEST_CASES_FILE}")
        
        os.makedirs(os.path.dirname(TEST_HISTORY_FILE), exist_ok=True)
        with open(TEST_HISTORY_FILE, "w") as f:
            json.dump(SAMPLE_TEST_HISTORY, f, indent=2)
        logger.info(f"Generated sample test history: {TEST_HISTORY_FILE}")
        
        return 0
    
    # Create and run the prioritizer
    prioritizer = TestPrioritizer()
    
    if not prioritizer.load_test_cases(args.test_cases):
        logger.error("Failed to load test cases")
        return 1
    
    if not prioritizer.load_test_history(args.test_history):
        logger.error("Failed to load test history")
        return 1
    
    prioritizer.prioritize_tests()
    
    # Save results
    prioritizer.save_prioritized_tests(args.output_json)
    prioritizer.export_to_csv(args.output_csv)
    prioritizer.export_to_markdown(args.output_md)
    
    logger.info("Test case prioritization complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())