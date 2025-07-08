#!/usr/bin/env python3
"""
Security Testing Script for OneTappe API

This script performs various security tests on the OneTappe API, including:
- Authentication bypass attempts
- SQL injection tests
- XSS vulnerability tests
- Input validation tests
- Rate limiting tests
- Error handling tests

The script generates a security report with findings and recommendations.
"""

import os
import sys
import json
import time
import datetime
import requests
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
RESULTS_DIR = "results"
SECURITY_REPORT_FILE = os.path.join(RESULTS_DIR, "security_report.md")
MAX_WORKERS = 5

# Test payloads
SQL_INJECTION_PAYLOADS = [
    "' OR 1=1 --",
    "\" OR 1=1 --",
    "1' OR '1'='1",
    "1\" OR \"1\"=\"1",
    "' OR '1'='1",
    "' OR 'a'='a",
    "\" OR \"a\"=\"a",
    "') OR ('a'='a",
    "1) OR (1=1",
    "; DROP TABLE users; --"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "<a onmouseover=alert('XSS')>click me</a>",
    "<body onload=alert('XSS')>",
    "<iframe src=javascript:alert('XSS')>",
    "<input value=\"<script>alert('XSS')</script>\">"
]

INVALID_INPUTS = [
    "" * 1000,  # Very long string
    "\x00\x01\x02\x03",  # Binary data
    "../../../etc/passwd",  # Path traversal
    "<?php echo 'hi'; ?>",  # Code injection
    "${{<%[%'}}%\\",  # Template injection
    "True",  # Boolean injection
    "None",  # Null injection
    "1e100",  # Number overflow
    "-1",  # Negative values
    "\u0000"  # Null byte
]


def ensure_server_running():
    """Ensure the API server is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        return response.status_code < 500
    except requests.RequestException:
        print("API server is not running. Starting server...")
        
        # Start the server in a separate process
        server_script = Path("../run_app.py").resolve()
        subprocess.Popen([sys.executable, str(server_script)], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        for _ in range(10):
            time.sleep(1)
            try:
                response = requests.get(f"{API_BASE_URL}/")
                if response.status_code < 500:
                    print("Server started successfully.")
                    return True
            except requests.RequestException:
                pass
        
        print("Failed to start server.")
        return False


def test_authentication_bypass():
    """Test for authentication bypass vulnerabilities."""
    print("Testing authentication bypass...")
    
    endpoints = [
        "/products",
        "/seller/dashboard",
        "/seller/orders",
        "/seller/inventory"
    ]
    
    results = []
    
    # Test accessing protected endpoints without authentication
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            
            # Check if authentication is properly enforced
            if response.status_code not in [401, 403]:
                results.append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "vulnerability": "Potential authentication bypass",
                    "details": "Endpoint accessible without authentication"
                })
        except requests.RequestException as e:
            results.append({
                "endpoint": endpoint,
                "status_code": "Error",
                "vulnerability": "Test failed",
                "details": str(e)
            })
    
    # Test with invalid tokens
    invalid_tokens = [
        "",  # Empty token
        "invalid_token",  # Random string
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",  # Sample JWT
        "Bearer ",  # Empty bearer token
        "Basic YWRtaW46YWRtaW4="  # Basic auth with admin:admin
    ]
    
    for token in invalid_tokens:
        for endpoint in endpoints:
            try:
                headers = {"Authorization": token}
                response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
                
                # Check if authentication is properly enforced
                if response.status_code not in [401, 403]:
                    results.append({
                        "endpoint": endpoint,
                        "token": token,
                        "status_code": response.status_code,
                        "vulnerability": "Potential authentication bypass",
                        "details": "Endpoint accessible with invalid token"
                    })
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "token": token,
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    return results


def test_sql_injection():
    """Test for SQL injection vulnerabilities."""
    print("Testing SQL injection...")
    
    endpoints = [
        "/products",
        "/products/1",
        "/login"
    ]
    
    results = []
    
    # Test GET endpoints
    for endpoint in endpoints:
        for payload in SQL_INJECTION_PAYLOADS:
            try:
                # Try in query parameters
                params = {"q": payload, "id": payload, "search": payload}
                response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
                
                # Look for signs of SQL injection vulnerability
                if any(sign in response.text.lower() for sign in ["sql syntax", "sqlite3.", "mysql", "postgresql", "syntax error", "unclosed quotation"]):
                    results.append({
                        "endpoint": endpoint,
                        "method": "GET",
                        "payload": payload,
                        "status_code": response.status_code,
                        "vulnerability": "Potential SQL injection",
                        "details": "SQL error message detected in response"
                    })
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "method": "GET",
                    "payload": payload,
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    # Test POST endpoints
    post_endpoints = [
        "/products",
        "/login"
    ]
    
    for endpoint in post_endpoints:
        for payload in SQL_INJECTION_PAYLOADS:
            try:
                # Try in JSON body
                data = {
                    "username": payload,
                    "password": payload,
                    "product_name": payload,
                    "price": 10.0,
                    "stock": 10,
                    "description": payload,
                    "seller_id": 1
                }
                
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
                
                # Look for signs of SQL injection vulnerability
                if any(sign in response.text.lower() for sign in ["sql syntax", "sqlite3.", "mysql", "postgresql", "syntax error", "unclosed quotation"]):
                    results.append({
                        "endpoint": endpoint,
                        "method": "POST",
                        "payload": payload,
                        "status_code": response.status_code,
                        "vulnerability": "Potential SQL injection",
                        "details": "SQL error message detected in response"
                    })
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "method": "POST",
                    "payload": payload,
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    return results


def test_xss_vulnerabilities():
    """Test for XSS vulnerabilities."""
    print("Testing XSS vulnerabilities...")
    
    endpoints = [
        "/products"
    ]
    
    results = []
    
    # Test POST endpoints for stored XSS
    for endpoint in endpoints:
        for payload in XSS_PAYLOADS:
            try:
                # Try to store XSS payload
                data = {
                    "product_name": payload,
                    "price": 10.0,
                    "stock": 10,
                    "description": payload,
                    "seller_id": 1
                }
                
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
                
                if response.status_code in [200, 201]:
                    # If successful, check if we can retrieve the payload
                    try:
                        product_id = response.json().get("id")
                        if product_id:
                            get_response = requests.get(f"{API_BASE_URL}{endpoint}/{product_id}")
                            
                            # Check if the payload is returned unescaped
                            if payload in get_response.text:
                                results.append({
                                    "endpoint": endpoint,
                                    "method": "POST/GET",
                                    "payload": payload,
                                    "status_code": response.status_code,
                                    "vulnerability": "Potential stored XSS",
                                    "details": "XSS payload stored and returned unescaped"
                                })
                    except (requests.RequestException, json.JSONDecodeError):
                        pass
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "method": "POST",
                    "payload": payload,
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    # Test GET endpoints for reflected XSS
    for endpoint in endpoints:
        for payload in XSS_PAYLOADS:
            try:
                # Try in query parameters
                params = {"q": payload, "search": payload}
                response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
                
                # Check if the payload is reflected unescaped
                if payload in response.text:
                    results.append({
                        "endpoint": endpoint,
                        "method": "GET",
                        "payload": payload,
                        "status_code": response.status_code,
                        "vulnerability": "Potential reflected XSS",
                        "details": "XSS payload reflected in response unescaped"
                    })
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "method": "GET",
                    "payload": payload,
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    return results


def test_input_validation():
    """Test input validation."""
    print("Testing input validation...")
    
    endpoints = [
        "/products"
    ]
    
    results = []
    
    # Test POST endpoints
    for endpoint in endpoints:
        for payload in INVALID_INPUTS:
            try:
                # Test with invalid product data
                data = {
                    "product_name": payload,
                    "price": payload,
                    "stock": payload,
                    "description": payload,
                    "seller_id": payload
                }
                
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
                
                # Check if proper validation is in place
                if response.status_code in [200, 201]:
                    results.append({
                        "endpoint": endpoint,
                        "method": "POST",
                        "payload": str(payload)[:30] + "...",
                        "status_code": response.status_code,
                        "vulnerability": "Potential input validation issue",
                        "details": "Invalid input accepted"
                    })
            except requests.RequestException as e:
                results.append({
                    "endpoint": endpoint,
                    "method": "POST",
                    "payload": str(payload)[:30] + "...",
                    "status_code": "Error",
                    "vulnerability": "Test failed",
                    "details": str(e)
                })
    
    return results


def test_rate_limiting():
    """Test for rate limiting."""
    print("Testing rate limiting...")
    
    endpoints = [
        "/products",
        "/login"
    ]
    
    results = []
    
    # Test each endpoint with multiple rapid requests
    for endpoint in endpoints:
        start_time = time.time()
        success_count = 0
        error_count = 0
        
        # Send 50 requests in quick succession
        for _ in range(50):
            try:
                response = requests.get(f"{API_BASE_URL}{endpoint}")
                if response.status_code < 400:
                    success_count += 1
                else:
                    error_count += 1
            except requests.RequestException:
                error_count += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check if all requests succeeded (indicating no rate limiting)
        if success_count == 50:
            results.append({
                "endpoint": endpoint,
                "method": "GET",
                "requests": 50,
                "duration": f"{duration:.2f}s",
                "vulnerability": "No rate limiting detected",
                "details": f"All {success_count} requests succeeded in {duration:.2f} seconds"
            })
    
    return results


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    endpoints = [
        "/products/999999",  # Non-existent product
        "/products/abc",  # Invalid ID format
        "/nonexistent/endpoint",  # Non-existent endpoint
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            
            # Check for proper error handling
            if response.status_code >= 500:
                results.append({
                    "endpoint": endpoint,
                    "method": "GET",
                    "status_code": response.status_code,
                    "vulnerability": "Improper error handling",
                    "details": "Server returned 5xx error instead of proper error response"
                })
            
            # Check for excessive information disclosure in error messages
            response_text = response.text.lower()
            if any(sign in response_text for sign in ["exception", "traceback", "stack trace", "at line", "syntax error", "error:"]):
                results.append({
                    "endpoint": endpoint,
                    "method": "GET",
                    "status_code": response.status_code,
                    "vulnerability": "Information disclosure",
                    "details": "Error response contains sensitive information"
                })
        except requests.RequestException as e:
            results.append({
                "endpoint": endpoint,
                "method": "GET",
                "status_code": "Error",
                "vulnerability": "Test failed",
                "details": str(e)
            })
    
    return results


def run_security_tests():
    """Run all security tests."""
    print("Running security tests...")
    
    # Ensure server is running
    if not ensure_server_running():
        print("Cannot run security tests without a running server.")
        return {}
    
    # Run tests in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        auth_bypass_future = executor.submit(test_authentication_bypass)
        sql_injection_future = executor.submit(test_sql_injection)
        xss_future = executor.submit(test_xss_vulnerabilities)
        input_validation_future = executor.submit(test_input_validation)
        rate_limiting_future = executor.submit(test_rate_limiting)
        error_handling_future = executor.submit(test_error_handling)
        
        # Collect results
        results = {
            "authentication_bypass": auth_bypass_future.result(),
            "sql_injection": sql_injection_future.result(),
            "xss": xss_future.result(),
            "input_validation": input_validation_future.result(),
            "rate_limiting": rate_limiting_future.result(),
            "error_handling": error_handling_future.result()
        }
    
    return results


def generate_security_report(results):
    """Generate a security report based on test results."""
    print("Generating security report...")
    
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Count vulnerabilities by severity
    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    
    # Categorize vulnerabilities by severity
    critical_vulns = []
    high_vulns = []
    medium_vulns = []
    low_vulns = []
    
    # Process results
    for category, findings in results.items():
        for finding in findings:
            # Determine severity based on vulnerability type
            severity = "Low"
            
            if category == "authentication_bypass":
                severity = "Critical"
                critical_count += 1
                critical_vulns.append(finding)
            elif category == "sql_injection":
                severity = "Critical"
                critical_count += 1
                critical_vulns.append(finding)
            elif category == "xss":
                severity = "High"
                high_count += 1
                high_vulns.append(finding)
            elif category == "input_validation":
                severity = "Medium"
                medium_count += 1
                medium_vulns.append(finding)
            elif category == "rate_limiting":
                severity = "Medium"
                medium_count += 1
                medium_vulns.append(finding)
            elif category == "error_handling":
                severity = "Low"
                low_count += 1
                low_vulns.append(finding)
    
    # Generate report
    report = f"# OneTappe API Security Test Report\n\n"
    report += f"**Date:** {current_date}\n"
    report += f"**Tester:** Automated Security Test\n\n"
    
    # Summary
    report += f"## Summary\n\n"
    report += f"| Severity | Count |\n"
    report += f"|----------|-------|\n"
    report += f"| Critical | {critical_count} |\n"
    report += f"| High | {high_count} |\n"
    report += f"| Medium | {medium_count} |\n"
    report += f"| Low | {low_count} |\n"
    report += f"| **Total** | **{critical_count + high_count + medium_count + low_count}** |\n\n"
    
    # Critical vulnerabilities
    if critical_vulns:
        report += f"## Critical Vulnerabilities\n\n"
        for i, vuln in enumerate(critical_vulns, 1):
            report += f"### {i}. {vuln['vulnerability']}\n\n"
            report += f"- **Endpoint:** {vuln['endpoint']}\n"
            report += f"- **Method:** {vuln.get('method', 'N/A')}\n"
            report += f"- **Status Code:** {vuln['status_code']}\n"
            if 'payload' in vuln:
                report += f"- **Payload:** `{vuln['payload']}`\n"
            report += f"- **Details:** {vuln['details']}\n\n"
    
    # High vulnerabilities
    if high_vulns:
        report += f"## High Vulnerabilities\n\n"
        for i, vuln in enumerate(high_vulns, 1):
            report += f"### {i}. {vuln['vulnerability']}\n\n"
            report += f"- **Endpoint:** {vuln['endpoint']}\n"
            report += f"- **Method:** {vuln.get('method', 'N/A')}\n"
            report += f"- **Status Code:** {vuln['status_code']}\n"
            if 'payload' in vuln:
                report += f"- **Payload:** `{vuln['payload']}`\n"
            report += f"- **Details:** {vuln['details']}\n\n"
    
    # Medium vulnerabilities
    if medium_vulns:
        report += f"## Medium Vulnerabilities\n\n"
        for i, vuln in enumerate(medium_vulns, 1):
            report += f"### {i}. {vuln['vulnerability']}\n\n"
            report += f"- **Endpoint:** {vuln['endpoint']}\n"
            report += f"- **Method:** {vuln.get('method', 'N/A')}\n"
            report += f"- **Status Code:** {vuln['status_code']}\n"
            if 'payload' in vuln:
                report += f"- **Payload:** `{vuln['payload']}`\n"
            report += f"- **Details:** {vuln['details']}\n\n"
    
    # Low vulnerabilities
    if low_vulns:
        report += f"## Low Vulnerabilities\n\n"
        for i, vuln in enumerate(low_vulns, 1):
            report += f"### {i}. {vuln['vulnerability']}\n\n"
            report += f"- **Endpoint:** {vuln['endpoint']}\n"
            report += f"- **Method:** {vuln.get('method', 'N/A')}\n"
            report += f"- **Status Code:** {vuln['status_code']}\n"
            if 'payload' in vuln:
                report += f"- **Payload:** `{vuln['payload']}`\n"
            report += f"- **Details:** {vuln['details']}\n\n"
    
    # Recommendations
    report += f"## Recommendations\n\n"
    
    if critical_count > 0 or high_count > 0:
        report += f"### Critical and High Priority\n\n"
        
        if any("authentication bypass" in vuln['vulnerability'].lower() for vuln in critical_vulns):
            report += f"1. **Implement proper authentication**: Ensure all protected endpoints require valid authentication.\n"
            report += f"   - Use JWT or OAuth for secure authentication\n"
            report += f"   - Validate tokens on every request\n"
            report += f"   - Implement proper token expiration and refresh mechanisms\n\n"
        
        if any("sql injection" in vuln['vulnerability'].lower() for vuln in critical_vulns):
            report += f"2. **Prevent SQL injection**: Use parameterized queries or ORM for all database operations.\n"
            report += f"   - Never concatenate user input directly into SQL queries\n"
            report += f"   - Use prepared statements with parameterized queries\n"
            report += f"   - Consider using an ORM like SQLAlchemy\n\n"
        
        if any("xss" in vuln['vulnerability'].lower() for vuln in high_vulns):
            report += f"3. **Prevent XSS vulnerabilities**: Sanitize and escape all user input before rendering.\n"
            report += f"   - Use content security policy (CSP) headers\n"
            report += f"   - Sanitize user input on both client and server sides\n"
            report += f"   - Use frameworks that automatically escape output\n\n"
    
    if medium_count > 0:
        report += f"### Medium Priority\n\n"
        
        if any("input validation" in vuln['vulnerability'].lower() for vuln in medium_vulns):
            report += f"1. **Improve input validation**: Implement strict validation for all user inputs.\n"
            report += f"   - Validate data types, ranges, and formats\n"
            report += f"   - Use validation libraries or frameworks\n"
            report += f"   - Implement both client-side and server-side validation\n\n"
        
        if any("rate limiting" in vuln['vulnerability'].lower() for vuln in medium_vulns):
            report += f"2. **Implement rate limiting**: Protect against brute force and DoS attacks.\n"
            report += f"   - Limit requests per IP address\n"
            report += f"   - Implement exponential backoff for failed authentication attempts\n"
            report += f"   - Consider using a rate limiting middleware\n\n"
    
    if low_count > 0:
        report += f"### Low Priority\n\n"
        
        if any("error handling" in vuln['vulnerability'].lower() for vuln in low_vulns):
            report += f"1. **Improve error handling**: Implement proper error handling to avoid information disclosure.\n"
            report += f"   - Use custom error handlers\n"
            report += f"   - Avoid exposing stack traces or detailed error messages\n"
            report += f"   - Log errors for debugging but return generic messages to users\n\n"
    
    # Conclusion
    report += f"## Conclusion\n\n"
    
    if critical_count > 0:
        report += f"The OneTappe API has **critical security vulnerabilities** that must be addressed immediately before deployment. "
    elif high_count > 0:
        report += f"The OneTappe API has **high security vulnerabilities** that should be addressed before deployment. "
    elif medium_count > 0:
        report += f"The OneTappe API has **some security issues** that should be addressed to improve security. "
    elif low_count > 0:
        report += f"The OneTappe API has **minor security issues** that could be improved. "
    else:
        report += f"The OneTappe API passed all security tests. No vulnerabilities were detected. "
    
    total_vulns = critical_count + high_count + medium_count + low_count
    report += f"A total of {total_vulns} potential security issues were identified.\n\n"
    
    # Write report to file
    with open(SECURITY_REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"Security report generated: {SECURITY_REPORT_FILE}")
    return report


def main():
    """Main function to run security tests and generate report."""
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Run security tests
    results = run_security_tests()
    
    # Save raw results
    with open(os.path.join(RESULTS_DIR, "security_test_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Generate security report
    generate_security_report(results)
    
    print("Done!")


if __name__ == "__main__":
    main()