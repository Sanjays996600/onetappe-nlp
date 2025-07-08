#!/usr/bin/env python3
"""
Test Coverage Report Generator for OneTappe API

This script generates a test coverage report for the OneTappe API.
It uses the coverage.py library to measure code coverage during test execution.
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

# Configuration
COVERAGE_CONFIG = """
[run]
source = ..
omit = */tests/*, */testing/*, */migrations/*, */venv/*, */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError

[html]
directory = coverage_html_report
"""


def setup_coverage():
    """Set up coverage configuration."""
    print("Setting up coverage configuration...")
    
    # Create coverage config file
    with open(".coveragerc", "w") as f:
        f.write(COVERAGE_CONFIG)
    
    # Ensure coverage is installed
    try:
        import coverage
    except ImportError:
        print("Coverage.py not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "coverage"])


def run_tests_with_coverage():
    """Run tests with coverage."""
    print("Running tests with coverage...")
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Run the tests with coverage
    cmd = [
        sys.executable, "-m", "coverage", "run", 
        "--source=..", "--omit=*/tests/*,*/testing/*,*/migrations/*,*/venv/*,*/env/*",
        "run_tests.py"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Save test output
    with open(os.path.join("results", "test_output.txt"), "w") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\n\nERRORS:\n")
            f.write(result.stderr)
    
    return result.returncode == 0


def generate_coverage_report():
    """Generate coverage reports in different formats."""
    print("Generating coverage reports...")
    
    # Generate coverage report in text format
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], 
                   capture_output=True, text=True)
    
    # Save coverage report to file
    result = subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], 
                          capture_output=True, text=True)
    
    with open(os.path.join("results", "coverage_report.txt"), "w") as f:
        f.write(result.stdout)
    
    # Generate HTML report
    subprocess.run([sys.executable, "-m", "coverage", "html"])
    
    # Generate XML report for CI integration
    subprocess.run([sys.executable, "-m", "coverage", "xml"])
    
    print(f"Coverage reports generated in {os.path.abspath('results')} and {os.path.abspath('coverage_html_report')}")


def generate_coverage_badge():
    """Generate a coverage badge based on the coverage percentage."""
    print("Generating coverage badge...")
    
    # Get coverage percentage
    result = subprocess.run([sys.executable, "-m", "coverage", "report"], 
                          capture_output=True, text=True)
    
    # Extract coverage percentage
    for line in result.stdout.split("\n"):
        if "TOTAL" in line:
            parts = line.split()
            if len(parts) >= 4:
                coverage_pct = parts[-1].strip("%")
                break
    else:
        coverage_pct = "0"
    
    # Determine badge color based on coverage percentage
    coverage_float = float(coverage_pct)
    if coverage_float >= 90:
        color = "brightgreen"
    elif coverage_float >= 80:
        color = "green"
    elif coverage_float >= 70:
        color = "yellowgreen"
    elif coverage_float >= 60:
        color = "yellow"
    else:
        color = "red"
    
    # Generate badge SVG
    badge_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="104" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="104" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h61v20H0z"/>
        <path fill="#{color}" d="M61 0h43v20H61z"/>
        <path fill="url(#b)" d="M0 0h104v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="30.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="30.5" y="14">coverage</text>
        <text x="82.5" y="15" fill="#010101" fill-opacity=".3">{coverage_pct}%</text>
        <text x="82.5" y="14">{coverage_pct}%</text>
    </g>
</svg>"""
    
    # Save badge SVG
    with open(os.path.join("results", "coverage-badge.svg"), "w") as f:
        f.write(badge_svg)
    
    print(f"Coverage badge generated: {coverage_pct}% coverage")


def generate_coverage_summary():
    """Generate a summary of the coverage report."""
    print("Generating coverage summary...")
    
    # Get coverage report
    result = subprocess.run([sys.executable, "-m", "coverage", "report"], 
                          capture_output=True, text=True)
    
    # Parse coverage report
    lines = result.stdout.split("\n")
    headers = []
    data = []
    total = {}
    
    for i, line in enumerate(lines):
        if i == 0:
            headers = [h.strip() for h in line.split("  ") if h.strip()]
        elif "TOTAL" in line:
            parts = line.split()
            total = {
                "name": "TOTAL",
                "statements": parts[-4],
                "missing": parts[-3],
                "excluded": parts[-2],
                "coverage": parts[-1]
            }
        elif line.strip() and not line.startswith("-"):
            parts = line.split()
            if len(parts) >= 5:
                data.append({
                    "name": parts[0],
                    "statements": parts[-4],
                    "missing": parts[-3],
                    "excluded": parts[-2],
                    "coverage": parts[-1]
                })
    
    # Generate summary markdown
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = f"# Coverage Report Summary\n\n"
    summary += f"Generated on: {now}\n\n"
    
    # Add total coverage badge
    summary += f"![Coverage](./coverage-badge.svg)\n\n"
    
    # Add summary table
    summary += "## Coverage Summary\n\n"
    summary += "| Module | Statements | Missing | Excluded | Coverage |\n"
    summary += "|--------|------------|---------|----------|----------|\n"
    
    for item in data:
        summary += f"| {item['name']} | {item['statements']} | {item['missing']} | {item['excluded']} | {item['coverage']} |\n"
    
    summary += f"| **TOTAL** | **{total['statements']}** | **{total['missing']}** | **{total['excluded']}** | **{total['coverage']}** |\n\n"
    
    # Add recommendations based on coverage
    summary += "## Recommendations\n\n"
    
    # Find modules with low coverage
    low_coverage_modules = []
    for item in data:
        coverage_pct = float(item['coverage'].strip("%"))
        if coverage_pct < 70:
            low_coverage_modules.append((item['name'], coverage_pct))
    
    if low_coverage_modules:
        summary += "### Modules with Low Coverage\n\n"
        for module, coverage in low_coverage_modules:
            summary += f"- **{module}**: {coverage}% coverage - Consider adding more tests\n"
    else:
        summary += "All modules have acceptable coverage levels.\n"
    
    # Save summary markdown
    with open(os.path.join("results", "coverage_summary.md"), "w") as f:
        f.write(summary)
    
    print("Coverage summary generated")


def main():
    """Main function to run coverage analysis and generate reports."""
    # Set up coverage configuration
    setup_coverage()
    
    # Run tests with coverage
    success = run_tests_with_coverage()
    
    if success:
        print("Tests completed successfully.")
    else:
        print("Tests completed with errors. See test output for details.")
    
    # Generate coverage reports
    generate_coverage_report()
    
    # Generate coverage badge
    generate_coverage_badge()
    
    # Generate coverage summary
    generate_coverage_summary()
    
    print("Done!")


if __name__ == "__main__":
    main()