#!/usr/bin/env python3
"""
Performance Testing Script for OneTappe API

This script performs various performance tests on the OneTappe API, including:
- Response time measurements
- Throughput testing
- Load testing
- Stress testing
- Endurance testing (simplified)

The script generates a performance report with metrics and recommendations.
"""

import os
import sys
import json
import time
import datetime
import statistics
import requests
import subprocess
import matplotlib.pyplot as plt
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
RESULTS_DIR = "results"
PERFORMANCE_REPORT_FILE = os.path.join(RESULTS_DIR, "performance_report.md")
MAX_WORKERS = 10

# Test configuration
RESPONSE_TIME_SAMPLES = 20
THROUGHPUT_DURATION = 10  # seconds
LOAD_TEST_USERS = [1, 5, 10, 20, 30]  # concurrent users
LOAD_TEST_DURATION = 30  # seconds per user level
STRESS_TEST_MAX_USERS = 50
STRESS_TEST_STEP = 5
STRESS_TEST_DURATION = 10  # seconds per step
ENDURANCE_TEST_USERS = 5
ENDURANCE_TEST_DURATION = 60  # seconds (in a real test, this would be hours)

# Test endpoints
ENDPOINTS = [
    {"name": "Get all products", "method": "GET", "path": "/products", "data": None},
    {"name": "Get product by ID", "method": "GET", "path": "/products/1", "data": None},
    {"name": "Add product", "method": "POST", "path": "/products", "data": {
        "product_name": "Performance Test Product",
        "price": 99.99,
        "stock": 100,
        "description": "Product created during performance testing",
        "seller_id": 1
    }},
    {"name": "Login", "method": "POST", "path": "/login", "data": {
        "username": "test_user",
        "password": "password123"
    }}
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


def make_request(endpoint):
    """Make a request to the specified endpoint and return response time."""
    method = endpoint["method"]
    url = f"{API_BASE_URL}{endpoint['path']}"
    data = endpoint.get("data")
    
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            "success": response.status_code < 400,
            "status_code": response.status_code,
            "response_time": response_time
        }
    except requests.RequestException as e:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            "success": False,
            "status_code": "Error",
            "response_time": response_time,
            "error": str(e)
        }


def test_response_time():
    """Test response time for each endpoint."""
    print("Testing response time...")
    
    results = {}
    
    for endpoint in ENDPOINTS:
        endpoint_name = endpoint["name"]
        print(f"  Testing {endpoint_name}...")
        
        response_times = []
        success_count = 0
        error_count = 0
        
        for _ in range(RESPONSE_TIME_SAMPLES):
            result = make_request(endpoint)
            
            if result["success"]:
                success_count += 1
            else:
                error_count += 1
            
            response_times.append(result["response_time"])
            time.sleep(0.2)  # Small delay between requests
        
        # Calculate statistics
        if response_times:
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            p90_time = sorted(response_times)[int(len(response_times) * 0.9)]
            p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
            p99_time = sorted(response_times)[int(len(response_times) * 0.99)] if len(response_times) >= 100 else max_time
        else:
            avg_time = min_time = max_time = p90_time = p95_time = p99_time = 0
        
        results[endpoint_name] = {
            "samples": len(response_times),
            "success_rate": (success_count / len(response_times)) * 100 if response_times else 0,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "p90_time": p90_time,
            "p95_time": p95_time,
            "p99_time": p99_time,
            "raw_times": response_times
        }
    
    return results


def test_throughput():
    """Test throughput for each endpoint."""
    print("Testing throughput...")
    
    results = {}
    
    for endpoint in ENDPOINTS:
        endpoint_name = endpoint["name"]
        print(f"  Testing {endpoint_name}...")
        
        success_count = 0
        error_count = 0
        response_times = []
        
        start_time = time.time()
        end_time = start_time + THROUGHPUT_DURATION
        
        # Make requests until the duration is reached
        while time.time() < end_time:
            result = make_request(endpoint)
            
            if result["success"]:
                success_count += 1
            else:
                error_count += 1
            
            response_times.append(result["response_time"])
        
        actual_duration = time.time() - start_time
        requests_per_second = (success_count + error_count) / actual_duration
        successful_requests_per_second = success_count / actual_duration
        
        # Calculate statistics
        if response_times:
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
        else:
            avg_time = min_time = max_time = 0
        
        results[endpoint_name] = {
            "duration": actual_duration,
            "total_requests": success_count + error_count,
            "successful_requests": success_count,
            "failed_requests": error_count,
            "requests_per_second": requests_per_second,
            "successful_requests_per_second": successful_requests_per_second,
            "avg_response_time": avg_time,
            "min_response_time": min_time,
            "max_response_time": max_time
        }
    
    return results


def load_test_worker(endpoint, results, stop_time):
    """Worker function for load testing."""
    while time.time() < stop_time:
        result = make_request(endpoint)
        results.append(result)


def test_load():
    """Test API under different load levels."""
    print("Running load tests...")
    
    results = {}
    
    for endpoint in ENDPOINTS:
        endpoint_name = endpoint["name"]
        print(f"  Testing {endpoint_name}...")
        
        endpoint_results = {}
        
        for num_users in LOAD_TEST_USERS:
            print(f"    Testing with {num_users} concurrent users...")
            
            all_results = []
            start_time = time.time()
            stop_time = start_time + LOAD_TEST_DURATION
            
            # Create and start worker threads
            with ThreadPoolExecutor(max_workers=num_users) as executor:
                futures = []
                for _ in range(num_users):
                    future = executor.submit(load_test_worker, endpoint, all_results, stop_time)
                    futures.append(future)
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()
            
            actual_duration = time.time() - start_time
            
            # Calculate statistics
            success_count = sum(1 for r in all_results if r["success"])
            error_count = len(all_results) - success_count
            
            if all_results:
                response_times = [r["response_time"] for r in all_results]
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
                p90_time = sorted(response_times)[int(len(response_times) * 0.9)]
                p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
                p99_time = sorted(response_times)[int(len(response_times) * 0.99)] if len(response_times) >= 100 else max_time
            else:
                avg_time = min_time = max_time = p90_time = p95_time = p99_time = 0
            
            requests_per_second = len(all_results) / actual_duration
            successful_requests_per_second = success_count / actual_duration
            
            endpoint_results[num_users] = {
                "duration": actual_duration,
                "total_requests": len(all_results),
                "successful_requests": success_count,
                "failed_requests": error_count,
                "requests_per_second": requests_per_second,
                "successful_requests_per_second": successful_requests_per_second,
                "avg_response_time": avg_time,
                "min_response_time": min_time,
                "max_response_time": max_time,
                "p90_response_time": p90_time,
                "p95_response_time": p95_time,
                "p99_response_time": p99_time
            }
        
        results[endpoint_name] = endpoint_results
    
    return results


def test_stress():
    """Test API under increasing load until failure or max users."""
    print("Running stress tests...")
    
    results = {}
    
    for endpoint in ENDPOINTS:
        endpoint_name = endpoint["name"]
        print(f"  Stress testing {endpoint_name}...")
        
        endpoint_results = {}
        breaking_point = None
        
        for num_users in range(STRESS_TEST_STEP, STRESS_TEST_MAX_USERS + 1, STRESS_TEST_STEP):
            print(f"    Testing with {num_users} concurrent users...")
            
            all_results = []
            start_time = time.time()
            stop_time = start_time + STRESS_TEST_DURATION
            
            # Create and start worker threads
            with ThreadPoolExecutor(max_workers=num_users) as executor:
                futures = []
                for _ in range(num_users):
                    future = executor.submit(load_test_worker, endpoint, all_results, stop_time)
                    futures.append(future)
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()
            
            actual_duration = time.time() - start_time
            
            # Calculate statistics
            success_count = sum(1 for r in all_results if r["success"])
            error_count = len(all_results) - success_count
            
            if all_results:
                response_times = [r["response_time"] for r in all_results]
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
            else:
                avg_time = min_time = max_time = 0
            
            requests_per_second = len(all_results) / actual_duration
            successful_requests_per_second = success_count / actual_duration
            success_rate = (success_count / len(all_results)) * 100 if all_results else 0
            
            endpoint_results[num_users] = {
                "duration": actual_duration,
                "total_requests": len(all_results),
                "successful_requests": success_count,
                "failed_requests": error_count,
                "requests_per_second": requests_per_second,
                "successful_requests_per_second": successful_requests_per_second,
                "success_rate": success_rate,
                "avg_response_time": avg_time,
                "min_response_time": min_time,
                "max_response_time": max_time
            }
            
            # Check if we've reached the breaking point (success rate < 80% or avg response time > 1000ms)
            if success_rate < 80 or avg_time > 1000:
                breaking_point = num_users
                print(f"    Breaking point reached at {num_users} users")
                break
        
        results[endpoint_name] = {
            "results": endpoint_results,
            "breaking_point": breaking_point or STRESS_TEST_MAX_USERS
        }
    
    return results


def test_endurance():
    """Test API under sustained load for a period of time."""
    print("Running endurance tests...")
    
    results = {}
    
    for endpoint in ENDPOINTS:
        endpoint_name = endpoint["name"]
        print(f"  Endurance testing {endpoint_name}...")
        
        all_results = []
        time_series = []
        start_time = time.time()
        stop_time = start_time + ENDURANCE_TEST_DURATION
        
        # Create and start worker threads
        with ThreadPoolExecutor(max_workers=ENDURANCE_TEST_USERS) as executor:
            futures = []
            for _ in range(ENDURANCE_TEST_USERS):
                future = executor.submit(load_test_worker, endpoint, all_results, stop_time)
                futures.append(future)
            
            # Monitor performance over time
            while time.time() < stop_time:
                current_time = time.time()
                elapsed = current_time - start_time
                
                # Wait a bit before taking the next measurement
                time.sleep(1)
                
                # Calculate current statistics
                current_results = [r for r in all_results if r.get("timestamp", 0) >= current_time - 1]
                
                if current_results:
                    success_count = sum(1 for r in current_results if r["success"])
                    response_times = [r["response_time"] for r in current_results]
                    avg_time = statistics.mean(response_times) if response_times else 0
                    
                    time_series.append({
                        "elapsed_seconds": elapsed,
                        "requests": len(current_results),
                        "success_rate": (success_count / len(current_results)) * 100 if current_results else 0,
                        "avg_response_time": avg_time
                    })
            
            # Wait for all futures to complete
            for future in futures:
                future.result()
        
        actual_duration = time.time() - start_time
        
        # Calculate overall statistics
        success_count = sum(1 for r in all_results if r["success"])
        error_count = len(all_results) - success_count
        
        if all_results:
            response_times = [r["response_time"] for r in all_results]
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
        else:
            avg_time = min_time = max_time = 0
        
        requests_per_second = len(all_results) / actual_duration
        successful_requests_per_second = success_count / actual_duration
        
        results[endpoint_name] = {
            "duration": actual_duration,
            "total_requests": len(all_results),
            "successful_requests": success_count,
            "failed_requests": error_count,
            "requests_per_second": requests_per_second,
            "successful_requests_per_second": successful_requests_per_second,
            "avg_response_time": avg_time,
            "min_response_time": min_time,
            "max_response_time": max_time,
            "time_series": time_series
        }
    
    return results


def generate_charts(results):
    """Generate charts for the performance test results."""
    print("Generating charts...")
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(RESULTS_DIR, "charts")
    os.makedirs(charts_dir, exist_ok=True)
    
    # Response Time Comparison Chart
    response_time_results = results.get("response_time", {})
    if response_time_results:
        plt.figure(figsize=(12, 6))
        
        endpoints = list(response_time_results.keys())
        avg_times = [response_time_results[endpoint]["avg_time"] for endpoint in endpoints]
        p90_times = [response_time_results[endpoint]["p90_time"] for endpoint in endpoints]
        
        x = range(len(endpoints))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], avg_times, width, label='Average')
        plt.bar([i + width/2 for i in x], p90_times, width, label='90th Percentile')
        
        plt.xlabel('Endpoint')
        plt.ylabel('Response Time (ms)')
        plt.title('Response Time Comparison')
        plt.xticks(x, endpoints, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        chart_path = os.path.join(charts_dir, "response_time_comparison.png")
        plt.savefig(chart_path)
        plt.close()
    
    # Throughput Comparison Chart
    throughput_results = results.get("throughput", {})
    if throughput_results:
        plt.figure(figsize=(12, 6))
        
        endpoints = list(throughput_results.keys())
        rps = [throughput_results[endpoint]["requests_per_second"] for endpoint in endpoints]
        
        plt.bar(endpoints, rps)
        plt.xlabel('Endpoint')
        plt.ylabel('Requests per Second')
        plt.title('Throughput Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        chart_path = os.path.join(charts_dir, "throughput_comparison.png")
        plt.savefig(chart_path)
        plt.close()
    
    # Load Test Response Time Chart
    load_test_results = results.get("load", {})
    if load_test_results:
        for endpoint, data in load_test_results.items():
            plt.figure(figsize=(10, 6))
            
            users = list(data.keys())
            avg_times = [data[u]["avg_response_time"] for u in users]
            p90_times = [data[u]["p90_response_time"] for u in users]
            
            plt.plot(users, avg_times, marker='o', label='Average')
            plt.plot(users, p90_times, marker='s', label='90th Percentile')
            
            plt.xlabel('Concurrent Users')
            plt.ylabel('Response Time (ms)')
            plt.title(f'Load Test Response Time - {endpoint}')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
            chart_path = os.path.join(charts_dir, f"load_test_response_time_{endpoint.replace(' ', '_')}.png")
            plt.savefig(chart_path)
            plt.close()
    
    # Stress Test Charts
    stress_test_results = results.get("stress", {})
    if stress_test_results:
        for endpoint, data in stress_test_results.items():
            endpoint_results = data.get("results", {})
            if endpoint_results:
                plt.figure(figsize=(12, 8))
                
                users = list(endpoint_results.keys())
                success_rates = [endpoint_results[u]["success_rate"] for u in users]
                avg_times = [endpoint_results[u]["avg_response_time"] for u in users]
                
                fig, ax1 = plt.subplots(figsize=(10, 6))
                
                color = 'tab:blue'
                ax1.set_xlabel('Concurrent Users')
                ax1.set_ylabel('Success Rate (%)', color=color)
                ax1.plot(users, success_rates, marker='o', color=color)
                ax1.tick_params(axis='y', labelcolor=color)
                
                ax2 = ax1.twinx()
                color = 'tab:red'
                ax2.set_ylabel('Response Time (ms)', color=color)
                ax2.plot(users, avg_times, marker='s', color=color)
                ax2.tick_params(axis='y', labelcolor=color)
                
                plt.title(f'Stress Test - {endpoint}')
                plt.grid(True)
                plt.tight_layout()
                
                chart_path = os.path.join(charts_dir, f"stress_test_{endpoint.replace(' ', '_')}.png")
                plt.savefig(chart_path)
                plt.close()
    
    # Endurance Test Charts
    endurance_test_results = results.get("endurance", {})
    if endurance_test_results:
        for endpoint, data in endurance_test_results.items():
            time_series = data.get("time_series", [])
            if time_series:
                plt.figure(figsize=(12, 8))
                
                elapsed = [point["elapsed_seconds"] for point in time_series]
                avg_times = [point["avg_response_time"] for point in time_series]
                success_rates = [point["success_rate"] for point in time_series]
                
                fig, ax1 = plt.subplots(figsize=(10, 6))
                
                color = 'tab:blue'
                ax1.set_xlabel('Elapsed Time (seconds)')
                ax1.set_ylabel('Response Time (ms)', color=color)
                ax1.plot(elapsed, avg_times, color=color)
                ax1.tick_params(axis='y', labelcolor=color)
                
                ax2 = ax1.twinx()
                color = 'tab:green'
                ax2.set_ylabel('Success Rate (%)', color=color)
                ax2.plot(elapsed, success_rates, color=color)
                ax2.tick_params(axis='y', labelcolor=color)
                ax2.set_ylim([0, 105])
                
                plt.title(f'Endurance Test - {endpoint}')
                plt.grid(True)
                plt.tight_layout()
                
                chart_path = os.path.join(charts_dir, f"endurance_test_{endpoint.replace(' ', '_')}.png")
                plt.savefig(chart_path)
                plt.close()
    
    return charts_dir


def generate_performance_report(results, charts_dir):
    """Generate a performance report based on test results."""
    print("Generating performance report...")
    
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Generate report
    report = f"# OneTappe API Performance Test Report\n\n"
    report += f"**Date:** {current_date}\n"
    report += f"**Tester:** Automated Performance Test\n\n"
    
    # Summary
    report += f"## Summary\n\n"
    
    # Response Time Summary
    response_time_results = results.get("response_time", {})
    if response_time_results:
        report += f"### Response Time Summary\n\n"
        report += f"| Endpoint | Avg (ms) | Min (ms) | Max (ms) | 90th % (ms) | 95th % (ms) | Success Rate (%) |\n"
        report += f"|----------|----------|----------|----------|------------|------------|-----------------|\n"
        
        for endpoint, data in response_time_results.items():
            report += f"| {endpoint} | {data['avg_time']:.2f} | {data['min_time']:.2f} | {data['max_time']:.2f} | {data['p90_time']:.2f} | {data['p95_time']:.2f} | {data['success_rate']:.2f} |\n"
    
    # Throughput Summary
    throughput_results = results.get("throughput", {})
    if throughput_results:
        report += f"\n### Throughput Summary\n\n"
        report += f"| Endpoint | Requests/sec | Successful Requests/sec | Success Rate (%) | Avg Response Time (ms) |\n"
        report += f"|----------|-------------|------------------------|-----------------|------------------------|\n"
        
        for endpoint, data in throughput_results.items():
            success_rate = (data["successful_requests"] / data["total_requests"]) * 100 if data["total_requests"] > 0 else 0
            report += f"| {endpoint} | {data['requests_per_second']:.2f} | {data['successful_requests_per_second']:.2f} | {success_rate:.2f} | {data['avg_response_time']:.2f} |\n"
    
    # Load Test Summary
    load_test_results = results.get("load", {})
    if load_test_results:
        report += f"\n### Load Test Summary\n\n"
        
        for endpoint, data in load_test_results.items():
            report += f"#### {endpoint}\n\n"
            report += f"| Concurrent Users | Requests/sec | Success Rate (%) | Avg Response Time (ms) | 90th % (ms) |\n"
            report += f"|------------------|-------------|-----------------|------------------------|------------|\n"
            
            for users, user_data in data.items():
                success_rate = (user_data["successful_requests"] / user_data["total_requests"]) * 100 if user_data["total_requests"] > 0 else 0
                report += f"| {users} | {user_data['requests_per_second']:.2f} | {success_rate:.2f} | {user_data['avg_response_time']:.2f} | {user_data['p90_response_time']:.2f} |\n"
            
            report += f"\n![Load Test Chart](charts/load_test_response_time_{endpoint.replace(' ', '_')}.png)\n\n"
    
    # Stress Test Summary
    stress_test_results = results.get("stress", {})
    if stress_test_results:
        report += f"\n### Stress Test Summary\n\n"
        report += f"| Endpoint | Breaking Point (users) | Max RPS | Max Success Rate (%) |\n"
        report += f"|----------|--------------------------|---------|----------------------|\n"
        
        for endpoint, data in stress_test_results.items():
            breaking_point = data.get("breaking_point", "N/A")
            endpoint_results = data.get("results", {})
            
            max_rps = 0
            max_success_rate = 0
            
            for user_data in endpoint_results.values():
                max_rps = max(max_rps, user_data["requests_per_second"])
                max_success_rate = max(max_success_rate, user_data["success_rate"])
            
            report += f"| {endpoint} | {breaking_point} | {max_rps:.2f} | {max_success_rate:.2f} |\n"
            
            report += f"\n![Stress Test Chart](charts/stress_test_{endpoint.replace(' ', '_')}.png)\n\n"
    
    # Endurance Test Summary
    endurance_test_results = results.get("endurance", {})
    if endurance_test_results:
        report += f"\n### Endurance Test Summary\n\n"
        report += f"| Endpoint | Duration (s) | Avg RPS | Success Rate (%) | Avg Response Time (ms) |\n"
        report += f"|----------|--------------|---------|-----------------|------------------------|\n"
        
        for endpoint, data in endurance_test_results.items():
            success_rate = (data["successful_requests"] / data["total_requests"]) * 100 if data["total_requests"] > 0 else 0
            report += f"| {endpoint} | {data['duration']:.2f} | {data['requests_per_second']:.2f} | {success_rate:.2f} | {data['avg_response_time']:.2f} |\n"
            
            report += f"\n![Endurance Test Chart](charts/endurance_test_{endpoint.replace(' ', '_')}.png)\n\n"
    
    # Performance Analysis
    report += f"\n## Performance Analysis\n\n"
    
    # Response Time Analysis
    if response_time_results:
        report += f"### Response Time Analysis\n\n"
        
        # Find endpoints with high response times
        high_response_time_endpoints = []
        for endpoint, data in response_time_results.items():
            if data["avg_time"] > 200:  # Threshold for high response time (200ms)
                high_response_time_endpoints.append((endpoint, data["avg_time"]))
        
        if high_response_time_endpoints:
            report += f"The following endpoints have high average response times:\n\n"
            for endpoint, avg_time in high_response_time_endpoints:
                report += f"- **{endpoint}**: {avg_time:.2f} ms\n"
            report += f"\nThese endpoints may benefit from optimization.\n\n"
        else:
            report += f"All endpoints have acceptable response times.\n\n"
    
    # Throughput Analysis
    if throughput_results:
        report += f"### Throughput Analysis\n\n"
        
        # Find endpoints with low throughput
        low_throughput_endpoints = []
        for endpoint, data in throughput_results.items():
            if data["requests_per_second"] < 10:  # Threshold for low throughput (10 RPS)
                low_throughput_endpoints.append((endpoint, data["requests_per_second"]))
        
        if low_throughput_endpoints:
            report += f"The following endpoints have low throughput:\n\n"
            for endpoint, rps in low_throughput_endpoints:
                report += f"- **{endpoint}**: {rps:.2f} requests/second\n"
            report += f"\nThese endpoints may benefit from optimization.\n\n"
        else:
            report += f"All endpoints have acceptable throughput.\n\n"
    
    # Load Test Analysis
    if load_test_results:
        report += f"### Load Test Analysis\n\n"
        
        # Analyze how response time scales with load
        scaling_issues = []
        for endpoint, data in load_test_results.items():
            users = sorted(data.keys())
            if len(users) >= 2:
                base_users = users[0]
                max_users = users[-1]
                
                base_time = data[base_users]["avg_response_time"]
                max_time = data[max_users]["avg_response_time"]
                
                # Check if response time increases more than 5x with load
                if max_time > base_time * 5:
                    scaling_issues.append((endpoint, base_users, max_users, base_time, max_time))
        
        if scaling_issues:
            report += f"The following endpoints show poor scaling with increased load:\n\n"
            for endpoint, base_users, max_users, base_time, max_time in scaling_issues:
                report += f"- **{endpoint}**: Response time increased from {base_time:.2f} ms at {base_users} users to {max_time:.2f} ms at {max_users} users ({(max_time/base_time):.1f}x increase)\n"
            report += f"\nThese endpoints may benefit from optimization for better scaling.\n\n"
        else:
            report += f"All endpoints scale well with increased load.\n\n"
    
    # Stress Test Analysis
    if stress_test_results:
        report += f"### Stress Test Analysis\n\n"
        
        # Analyze breaking points
        low_breaking_points = []
        for endpoint, data in stress_test_results.items():
            breaking_point = data.get("breaking_point", STRESS_TEST_MAX_USERS)
            if breaking_point < 20:  # Threshold for low breaking point (20 users)
                low_breaking_points.append((endpoint, breaking_point))
        
        if low_breaking_points:
            report += f"The following endpoints have low breaking points:\n\n"
            for endpoint, breaking_point in low_breaking_points:
                report += f"- **{endpoint}**: Breaking point at {breaking_point} concurrent users\n"
            report += f"\nThese endpoints may benefit from optimization for better stress handling.\n\n"
        else:
            report += f"All endpoints handle stress well.\n\n"
    
    # Endurance Test Analysis
    if endurance_test_results:
        report += f"### Endurance Test Analysis\n\n"
        
        # Analyze performance degradation over time
        degradation_issues = []
        for endpoint, data in endurance_test_results.items():
            time_series = data.get("time_series", [])
            if len(time_series) >= 10:  # Need enough data points
                early_points = time_series[:5]
                late_points = time_series[-5:]
                
                early_avg_time = statistics.mean([point["avg_response_time"] for point in early_points])
                late_avg_time = statistics.mean([point["avg_response_time"] for point in late_points])
                
                # Check if response time increases more than 50% over time
                if late_avg_time > early_avg_time * 1.5:
                    degradation_issues.append((endpoint, early_avg_time, late_avg_time))
        
        if degradation_issues:
            report += f"The following endpoints show performance degradation over time:\n\n"
            for endpoint, early_time, late_time in degradation_issues:
                report += f"- **{endpoint}**: Response time increased from {early_time:.2f} ms to {late_time:.2f} ms ({(late_time/early_time):.1f}x increase)\n"
            report += f"\nThese endpoints may have memory leaks or resource exhaustion issues.\n\n"
        else:
            report += f"All endpoints maintain stable performance over time.\n\n"
    
    # Recommendations
    report += f"## Recommendations\n\n"
    
    recommendations = []
    
    # Response time recommendations
    if response_time_results:
        high_response_time_endpoints = [endpoint for endpoint, data in response_time_results.items() if data["avg_time"] > 200]
        if high_response_time_endpoints:
            recommendations.append(f"Optimize the following endpoints for better response time: {', '.join(high_response_time_endpoints)}")
    
    # Throughput recommendations
    if throughput_results:
        low_throughput_endpoints = [endpoint for endpoint, data in throughput_results.items() if data["requests_per_second"] < 10]
        if low_throughput_endpoints:
            recommendations.append(f"Improve throughput for the following endpoints: {', '.join(low_throughput_endpoints)}")
    
    # Load test recommendations
    if load_test_results and any(scaling_issues):
        recommendations.append("Implement caching for frequently accessed data to improve performance under load")
        recommendations.append("Consider optimizing database queries that might be causing performance bottlenecks")
    
    # Stress test recommendations
    if stress_test_results and any(low_breaking_points):
        recommendations.append("Implement connection pooling to handle more concurrent connections")
        recommendations.append("Consider implementing rate limiting to protect the API from being overwhelmed")
    
    # Endurance test recommendations
    if endurance_test_results and any(degradation_issues):
        recommendations.append("Check for memory leaks or resource exhaustion issues")
        recommendations.append("Implement proper resource cleanup and connection handling")
    
    # General recommendations
    recommendations.append("Implement monitoring and alerting for API performance metrics")
    recommendations.append("Set up regular performance testing as part of the CI/CD pipeline")
    
    # Add recommendations to report
    for i, recommendation in enumerate(recommendations, 1):
        report += f"{i}. {recommendation}\n"
    
    # Conclusion
    report += f"\n## Conclusion\n\n"
    
    # Determine overall performance assessment
    if response_time_results and throughput_results:
        high_response_time_count = sum(1 for data in response_time_results.values() if data["avg_time"] > 200)
        low_throughput_count = sum(1 for data in throughput_results.values() if data["requests_per_second"] < 10)
        
        if high_response_time_count == 0 and low_throughput_count == 0:
            report += f"The OneTappe API demonstrates good overall performance with acceptable response times and throughput. "
        elif high_response_time_count > len(response_time_results) / 2 or low_throughput_count > len(throughput_results) / 2:
            report += f"The OneTappe API shows significant performance issues that need to be addressed before deployment. "
        else:
            report += f"The OneTappe API shows mixed performance results with some endpoints performing well and others needing optimization. "
    
    if stress_test_results:
        low_breaking_point_count = sum(1 for data in stress_test_results.values() if data.get("breaking_point", STRESS_TEST_MAX_USERS) < 20)
        
        if low_breaking_point_count == 0:
            report += f"The API handles concurrent users well and shows good stress tolerance. "
        elif low_breaking_point_count > len(stress_test_results) / 2:
            report += f"The API shows poor handling of concurrent users and may struggle under heavy load. "
        else:
            report += f"Some API endpoints may struggle under heavy load and should be optimized. "
    
    if endurance_test_results:
        degradation_count = sum(1 for data in endurance_test_results.values() if any(degradation_issues))
        
        if degradation_count == 0:
            report += f"The API maintains stable performance over time without degradation. "
        else:
            report += f"Some API endpoints show performance degradation over time, suggesting potential resource management issues. "
    
    report += f"\nOverall, the API {len(recommendations) < 5 and 'is performing well but has some areas for improvement' or 'requires optimization in several areas before it can be considered production-ready'}."
    
    # Write report to file
    with open(PERFORMANCE_REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"Performance report generated: {PERFORMANCE_REPORT_FILE}")
    return report


def run_performance_tests():
    """Run all performance tests."""
    print("Running performance tests...")
    
    # Ensure server is running
    if not ensure_server_running():
        print("Cannot run performance tests without a running server.")
        return {}
    
    # Run tests
    results = {
        "response_time": test_response_time(),
        "throughput": test_throughput(),
        "load": test_load(),
        "stress": test_stress(),
        "endurance": test_endurance()
    }
    
    return results


def main():
    """Main function to run performance tests and generate report."""
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Run performance tests
    results = run_performance_tests()
    
    # Save raw results
    with open(os.path.join(RESULTS_DIR, "performance_test_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Generate charts
    charts_dir = generate_charts(results)
    
    # Generate performance report
    generate_performance_report(results, charts_dir)
    
    print("Done!")


if __name__ == "__main__":
    main()