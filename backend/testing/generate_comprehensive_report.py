#!/usr/bin/env python3
"""
Comprehensive API Test Report Generator for OneTappe

This script generates a comprehensive test report by combining results from:
- Functional tests (API endpoint tests)
- Performance tests
- Load tests
- Security tests
- Coverage reports

The report is generated in Markdown format and includes:
- Executive summary
- Test coverage metrics
- Functional test results
- Performance metrics
- Security findings
- Issues and recommendations
"""

import os
import sys
import json
import time
import datetime
import subprocess
import logging
from pathlib import Path

# Configuration
RESULTS_DIR = "results"
REPORT_FILE = os.path.join(RESULTS_DIR, "comprehensive_test_report.md")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(RESULTS_DIR, "report_generation.log"))
    ]
)
logger = logging.getLogger("report_generator")


def ensure_results_dir():
    """Ensure the results directory exists."""
    os.makedirs(RESULTS_DIR, exist_ok=True)


def run_test_suite():
    """Run the complete test suite and collect results."""
    logger.info("Running complete test suite...")
    
    # Dictionary to store all test results
    results = {}
    
    # Run functional tests
    logger.info("Running functional tests...")
    try:
        run_tests_script = Path("run_tests.py").resolve()
        process = subprocess.run(
            [sys.executable, str(run_tests_script)],
            capture_output=True,
            text=True,
            check=False
        )
        
        results["functional_tests"] = {
            "exit_code": process.returncode,
            "output": process.stdout,
            "error": process.stderr,
            "success": process.returncode == 0
        }
        
        logger.info(f"Functional tests completed with exit code {process.returncode}")
    except Exception as e:
        logger.error(f"Error running functional tests: {str(e)}")
        results["functional_tests"] = {
            "exit_code": -1,
            "output": "",
            "error": str(e),
            "success": False
        }
    
    # Run performance tests
    logger.info("Running performance tests...")
    try:
        performance_test_script = Path("performance_test.py").resolve()
        process = subprocess.run(
            [sys.executable, str(performance_test_script)],
            capture_output=True,
            text=True,
            check=False
        )
        
        results["performance_tests"] = {
            "exit_code": process.returncode,
            "output": process.stdout,
            "error": process.stderr,
            "success": process.returncode == 0
        }
        
        # Try to load performance test results
        performance_results_file = os.path.join(RESULTS_DIR, "performance_test_results.json")
        if os.path.exists(performance_results_file):
            with open(performance_results_file, "r") as f:
                results["performance_data"] = json.load(f)
        
        logger.info(f"Performance tests completed with exit code {process.returncode}")
    except Exception as e:
        logger.error(f"Error running performance tests: {str(e)}")
        results["performance_tests"] = {
            "exit_code": -1,
            "output": "",
            "error": str(e),
            "success": False
        }
    
    # Run security tests
    logger.info("Running security tests...")
    try:
        security_test_script = Path("security_test.py").resolve()
        process = subprocess.run(
            [sys.executable, str(security_test_script)],
            capture_output=True,
            text=True,
            check=False
        )
        
        results["security_tests"] = {
            "exit_code": process.returncode,
            "output": process.stdout,
            "error": process.stderr,
            "success": process.returncode == 0
        }
        
        # Try to load security test results
        security_report_file = os.path.join(RESULTS_DIR, "security_report.md")
        if os.path.exists(security_report_file):
            with open(security_report_file, "r") as f:
                results["security_report"] = f.read()
        
        logger.info(f"Security tests completed with exit code {process.returncode}")
    except Exception as e:
        logger.error(f"Error running security tests: {str(e)}")
        results["security_tests"] = {
            "exit_code": -1,
            "output": "",
            "error": str(e),
            "success": False
        }
    
    # Generate coverage report
    logger.info("Generating coverage report...")
    try:
        coverage_script = Path("generate_coverage_report.py").resolve()
        process = subprocess.run(
            [sys.executable, str(coverage_script)],
            capture_output=True,
            text=True,
            check=False
        )
        
        results["coverage"] = {
            "exit_code": process.returncode,
            "output": process.stdout,
            "error": process.stderr,
            "success": process.returncode == 0
        }
        
        # Try to load coverage summary
        coverage_summary_file = os.path.join(RESULTS_DIR, "coverage_summary.json")
        if os.path.exists(coverage_summary_file):
            with open(coverage_summary_file, "r") as f:
                results["coverage_data"] = json.load(f)
        
        logger.info(f"Coverage report generated with exit code {process.returncode}")
    except Exception as e:
        logger.error(f"Error generating coverage report: {str(e)}")
        results["coverage"] = {
            "exit_code": -1,
            "output": "",
            "error": str(e),
            "success": False
        }
    
    return results


def parse_functional_test_results(results):
    """Parse functional test results from the output."""
    functional_tests = results.get("functional_tests", {})
    output = functional_tests.get("output", "")
    
    # Initialize counters
    test_summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "details": []
    }
    
    # Try to extract test results from output
    # This is a simple parser and might need adjustment based on actual output format
    for line in output.split("\n"):
        if "PASSED" in line:
            test_summary["passed"] += 1
            test_summary["total"] += 1
            test_summary["details"].append({"name": line.split("PASSED")[0].strip(), "status": "PASSED"})
        elif "FAILED" in line:
            test_summary["failed"] += 1
            test_summary["total"] += 1
            test_summary["details"].append({"name": line.split("FAILED")[0].strip(), "status": "FAILED"})
        elif "ERROR" in line:
            test_summary["errors"] += 1
            test_summary["total"] += 1
            test_summary["details"].append({"name": line.split("ERROR")[0].strip(), "status": "ERROR"})
        elif "SKIPPED" in line:
            test_summary["skipped"] += 1
            test_summary["total"] += 1
            test_summary["details"].append({"name": line.split("SKIPPED")[0].strip(), "status": "SKIPPED"})
    
    # If we couldn't parse any tests but have a success flag, provide a basic summary
    if test_summary["total"] == 0 and functional_tests.get("success", False):
        test_summary["passed"] = 1
        test_summary["total"] = 1
        test_summary["details"].append({"name": "Functional Tests", "status": "PASSED"})
    
    return test_summary


def extract_performance_metrics(results):
    """Extract key performance metrics from performance test results."""
    performance_data = results.get("performance_data", {})
    
    metrics = {
        "response_time": {},
        "throughput": {},
        "load_test": {},
        "stress_test": {},
        "breaking_points": {}
    }
    
    # Extract response time metrics
    response_time_results = performance_data.get("response_time", {})
    for endpoint, data in response_time_results.items():
        metrics["response_time"][endpoint] = {
            "avg": data.get("avg_time", 0),
            "min": data.get("min_time", 0),
            "max": data.get("max_time", 0),
            "p90": data.get("p90_time", 0),
            "p95": data.get("p95_time", 0),
            "success_rate": data.get("success_rate", 0)
        }
    
    # Extract throughput metrics
    throughput_results = performance_data.get("throughput", {})
    for endpoint, data in throughput_results.items():
        metrics["throughput"][endpoint] = {
            "requests_per_second": data.get("requests_per_second", 0),
            "successful_requests_per_second": data.get("successful_requests_per_second", 0)
        }
    
    # Extract stress test breaking points
    stress_test_results = performance_data.get("stress", {})
    for endpoint, data in stress_test_results.items():
        metrics["breaking_points"][endpoint] = data.get("breaking_point", "N/A")
    
    return metrics


def extract_security_findings(results):
    """Extract security findings from security test results."""
    security_report = results.get("security_report", "")
    
    findings = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }
    
    # Simple parser for security findings
    # This assumes a specific format in the security report
    current_severity = None
    current_finding = None
    
    for line in security_report.split("\n"):
        if "# Critical Findings" in line:
            current_severity = "critical"
        elif "# High Severity Findings" in line:
            current_severity = "high"
        elif "# Medium Severity Findings" in line:
            current_severity = "medium"
        elif "# Low Severity Findings" in line:
            current_severity = "low"
        elif line.startswith("## ") and current_severity:
            current_finding = line.replace("## ", "").strip()
            findings[current_severity].append({"name": current_finding, "description": ""})
        elif current_finding and current_severity and line.strip() and not line.startswith("#"):
            if findings[current_severity] and findings[current_severity][-1]["name"] == current_finding:
                findings[current_severity][-1]["description"] += line + "\n"
    
    return findings


def extract_coverage_data(results):
    """Extract coverage data from coverage report."""
    coverage_data = results.get("coverage_data", {})
    
    coverage = {
        "total": coverage_data.get("total_coverage", 0),
        "by_file": coverage_data.get("file_coverage", {}),
        "by_type": {
            "statements": coverage_data.get("statement_coverage", 0),
            "branches": coverage_data.get("branch_coverage", 0),
            "functions": coverage_data.get("function_coverage", 0)
        }
    }
    
    return coverage


def identify_issues_and_recommendations(results, metrics, findings, coverage):
    """Identify issues and provide recommendations based on test results."""
    issues = []
    recommendations = []
    
    # Check functional test failures
    functional_tests = parse_functional_test_results(results)
    if functional_tests["failed"] > 0 or functional_tests["errors"] > 0:
        issues.append({
            "severity": "high",
            "description": f"Functional tests have {functional_tests['failed']} failures and {functional_tests['errors']} errors."
        })
        recommendations.append("Fix failing functional tests before deployment.")
    
    # Check performance issues
    for endpoint, data in metrics["response_time"].items():
        if data["avg"] > 200:  # Threshold for high response time (200ms)
            issues.append({
                "severity": "medium",
                "description": f"High average response time for {endpoint}: {data['avg']:.2f} ms."
            })
            recommendations.append(f"Optimize the {endpoint} endpoint for better response time.")
    
    # Check breaking points
    for endpoint, breaking_point in metrics["breaking_points"].items():
        if breaking_point != "N/A" and breaking_point < 20:  # Threshold for low breaking point (20 users)
            issues.append({
                "severity": "high",
                "description": f"Low breaking point for {endpoint}: {breaking_point} concurrent users."
            })
            recommendations.append(f"Improve scalability of the {endpoint} endpoint.")
    
    # Check security findings
    if findings["critical"]:
        for finding in findings["critical"]:
            issues.append({
                "severity": "critical",
                "description": f"Critical security finding: {finding['name']}"
            })
            recommendations.append(f"Address critical security issue: {finding['name']}")
    
    if findings["high"]:
        for finding in findings["high"]:
            issues.append({
                "severity": "high",
                "description": f"High severity security finding: {finding['name']}"
            })
            recommendations.append(f"Address high severity security issue: {finding['name']}")
    
    # Check coverage
    if coverage["total"] < 80:  # Threshold for acceptable coverage (80%)
        issues.append({
            "severity": "medium",
            "description": f"Low test coverage: {coverage['total']:.2f}%"
        })
        recommendations.append("Increase test coverage to at least 80%.")
    
    # Add general recommendations
    recommendations.append("Implement monitoring and alerting for API performance metrics.")
    recommendations.append("Set up regular performance testing as part of the CI/CD pipeline.")
    recommendations.append("Conduct regular security assessments.")
    
    return issues, recommendations


def generate_report(results):
    """Generate a comprehensive test report."""
    logger.info("Generating comprehensive test report...")
    
    # Parse test results
    functional_tests = parse_functional_test_results(results)
    performance_metrics = extract_performance_metrics(results)
    security_findings = extract_security_findings(results)
    coverage_data = extract_coverage_data(results)
    
    # Identify issues and recommendations
    issues, recommendations = identify_issues_and_recommendations(
        results, performance_metrics, security_findings, coverage_data
    )
    
    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Generate report
    report = f"# OneTappe API Comprehensive Test Report\n\n"
    report += f"**Date:** {current_date}\n"
    report += f"**Tester:** Automated Test Suite\n\n"
    
    # Executive Summary
    report += f"## Executive Summary\n\n"
    
    # Calculate overall status
    critical_issues = sum(1 for issue in issues if issue["severity"] == "critical")
    high_issues = sum(1 for issue in issues if issue["severity"] == "high")
    medium_issues = sum(1 for issue in issues if issue["severity"] == "medium")
    low_issues = sum(1 for issue in issues if issue["severity"] == "low")
    
    if critical_issues > 0:
        overall_status = "❌ CRITICAL ISSUES"
    elif high_issues > 0:
        overall_status = "⚠️ MAJOR ISSUES"
    elif medium_issues > 0 or functional_tests["failed"] > 0:
        overall_status = "⚠️ MINOR ISSUES"
    else:
        overall_status = "✅ PASSED"
    
    report += f"**Overall Status:** {overall_status}\n\n"
    
    report += f"This report summarizes the results of automated testing performed on the OneTappe API. "
    report += f"The testing included functional tests, performance tests, security tests, and code coverage analysis.\n\n"
    
    report += f"**Summary of Findings:**\n\n"
    report += f"- Functional Tests: {functional_tests['passed']}/{functional_tests['total']} passed "
    report += f"({functional_tests['failed']} failed, {functional_tests['errors']} errors, {functional_tests['skipped']} skipped)\n"
    report += f"- Code Coverage: {coverage_data['total']:.2f}%\n"
    report += f"- Security: {len(security_findings['critical'])} critical, {len(security_findings['high'])} high, "
    report += f"{len(security_findings['medium'])} medium, {len(security_findings['low'])} low severity findings\n"
    report += f"- Issues Identified: {critical_issues} critical, {high_issues} high, {medium_issues} medium, {low_issues} low severity\n\n"
    
    # Test Coverage
    report += f"## Test Coverage\n\n"
    report += f"**Overall Coverage:** {coverage_data['total']:.2f}%\n\n"
    report += f"**Coverage by Type:**\n\n"
    report += f"- Statements: {coverage_data['by_type']['statements']:.2f}%\n"
    report += f"- Branches: {coverage_data['by_type']['branches']:.2f}%\n"
    report += f"- Functions: {coverage_data['by_type']['functions']:.2f}%\n\n"
    
    report += f"**Coverage by File:**\n\n"
    report += f"| File | Coverage |\n"
    report += f"|------|----------|\n"
    
    for file, coverage in coverage_data["by_file"].items():
        report += f"| {file} | {coverage:.2f}% |\n"
    
    # Functional Test Results
    report += f"\n## Functional Test Results\n\n"
    report += f"**Summary:** {functional_tests['passed']}/{functional_tests['total']} tests passed "
    report += f"({functional_tests['failed']} failed, {functional_tests['errors']} errors, {functional_tests['skipped']} skipped)\n\n"
    
    report += f"**Test Details:**\n\n"
    report += f"| Test | Status |\n"
    report += f"|------|--------|\n"
    
    for test in functional_tests["details"]:
        status_icon = "✅" if test["status"] == "PASSED" else "❌" if test["status"] == "FAILED" or test["status"] == "ERROR" else "⚠️"
        report += f"| {test['name']} | {status_icon} {test['status']} |\n"
    
    # Performance Metrics
    report += f"\n## Performance Metrics\n\n"
    
    # Response Time
    report += f"### Response Time\n\n"
    report += f"| Endpoint | Avg (ms) | Min (ms) | Max (ms) | 90th % (ms) | 95th % (ms) | Success Rate (%) |\n"
    report += f"|----------|----------|----------|----------|------------|------------|-----------------|\n"
    
    for endpoint, data in performance_metrics["response_time"].items():
        report += f"| {endpoint} | {data['avg']:.2f} | {data['min']:.2f} | {data['max']:.2f} | {data['p90']:.2f} | {data['p95']:.2f} | {data['success_rate']:.2f} |\n"
    
    # Throughput
    report += f"\n### Throughput\n\n"
    report += f"| Endpoint | Requests/sec | Successful Requests/sec |\n"
    report += f"|----------|-------------|------------------------|\n"
    
    for endpoint, data in performance_metrics["throughput"].items():
        report += f"| {endpoint} | {data['requests_per_second']:.2f} | {data['successful_requests_per_second']:.2f} |\n"
    
    # Breaking Points
    report += f"\n### Stress Test Breaking Points\n\n"
    report += f"| Endpoint | Breaking Point (concurrent users) |\n"
    report += f"|----------|-------------------------------------|\n"
    
    for endpoint, breaking_point in performance_metrics["breaking_points"].items():
        report += f"| {endpoint} | {breaking_point} |\n"
    
    # Security Findings
    report += f"\n## Security Findings\n\n"
    
    # Critical Findings
    if security_findings["critical"]:
        report += f"### Critical Findings\n\n"
        for finding in security_findings["critical"]:
            report += f"#### {finding['name']}\n\n"
            report += f"{finding['description']}\n\n"
    else:
        report += f"### Critical Findings\n\n"
        report += f"No critical security findings.\n\n"
    
    # High Severity Findings
    if security_findings["high"]:
        report += f"### High Severity Findings\n\n"
        for finding in security_findings["high"]:
            report += f"#### {finding['name']}\n\n"
            report += f"{finding['description']}\n\n"
    else:
        report += f"### High Severity Findings\n\n"
        report += f"No high severity security findings.\n\n"
    
    # Medium Severity Findings
    if security_findings["medium"]:
        report += f"### Medium Severity Findings\n\n"
        for finding in security_findings["medium"]:
            report += f"#### {finding['name']}\n\n"
            report += f"{finding['description']}\n\n"
    else:
        report += f"### Medium Severity Findings\n\n"
        report += f"No medium severity security findings.\n\n"
    
    # Low Severity Findings
    if security_findings["low"]:
        report += f"### Low Severity Findings\n\n"
        for finding in security_findings["low"]:
            report += f"#### {finding['name']}\n\n"
            report += f"{finding['description']}\n\n"
    else:
        report += f"### Low Severity Findings\n\n"
        report += f"No low severity security findings.\n\n"
    
    # Issues and Recommendations
    report += f"## Issues and Recommendations\n\n"
    
    # Issues
    report += f"### Issues Identified\n\n"
    
    if issues:
        for issue in issues:
            severity_icon = "🔴" if issue["severity"] == "critical" else "🟠" if issue["severity"] == "high" else "🟡" if issue["severity"] == "medium" else "🟢"
            report += f"- {severity_icon} **{issue['severity'].upper()}:** {issue['description']}\n"
    else:
        report += f"No significant issues identified.\n"
    
    # Recommendations
    report += f"\n### Recommendations\n\n"
    
    for i, recommendation in enumerate(recommendations, 1):
        report += f"{i}. {recommendation}\n"
    
    # Conclusion
    report += f"\n## Conclusion\n\n"
    
    if overall_status == "✅ PASSED":
        report += f"The OneTappe API demonstrates good overall quality with acceptable test coverage, performance, and security. "
        report += f"The API is ready for deployment, but regular testing should continue as part of the development lifecycle.\n"
    elif overall_status == "⚠️ MINOR ISSUES":
        report += f"The OneTappe API shows generally good quality but has some minor issues that should be addressed. "
        report += f"These issues are not blocking for deployment but should be fixed in upcoming releases.\n"
    elif overall_status == "⚠️ MAJOR ISSUES":
        report += f"The OneTappe API has significant issues that should be addressed before deployment. "
        report += f"These issues could impact user experience or system stability.\n"
    else:  # CRITICAL ISSUES
        report += f"The OneTappe API has critical issues that must be fixed before deployment. "
        report += f"These issues could lead to security vulnerabilities, data loss, or system failure.\n"
    
    # Appendix
    report += f"\n## Appendix\n\n"
    
    # Test Environment
    report += f"### Test Environment\n\n"
    report += f"- **Operating System:** {os.name} {sys.platform}\n"
    report += f"- **Python Version:** {sys.version.split()[0]}\n"
    report += f"- **Test Date:** {current_date}\n"
    
    # Write report to file
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    logger.info(f"Comprehensive test report generated: {REPORT_FILE}")
    return report


def main():
    """Main function to run tests and generate report."""
    # Ensure results directory exists
    ensure_results_dir()
    
    # Check if we should run tests or just generate report from existing results
    run_tests = len(sys.argv) > 1 and sys.argv[1] == "--run-tests"
    
    if run_tests:
        # Run tests and collect results
        results = run_test_suite()
        
        # Save raw results
        with open(os.path.join(RESULTS_DIR, "test_results.json"), "w") as f:
            # Convert non-serializable objects to strings
            serializable_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    serializable_results[key] = {}
                    for k, v in value.items():
                        if isinstance(v, (str, int, float, bool, list, dict)) or v is None:
                            serializable_results[key][k] = v
                        else:
                            serializable_results[key][k] = str(v)
                else:
                    if isinstance(value, (str, int, float, bool, list, dict)) or value is None:
                        serializable_results[key] = value
                    else:
                        serializable_results[key] = str(value)
            
            json.dump(serializable_results, f, indent=2)
    else:
        # Try to load existing results
        results_file = os.path.join(RESULTS_DIR, "test_results.json")
        if os.path.exists(results_file):
            with open(results_file, "r") as f:
                results = json.load(f)
        else:
            logger.error(f"No existing test results found at {results_file}")
            logger.error("Run with --run-tests to generate results")
            return 1
    
    # Generate report
    generate_report(results)
    
    logger.info("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())