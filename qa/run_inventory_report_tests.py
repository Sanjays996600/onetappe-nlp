#!/usr/bin/env python3
"""
Inventory Report Test Runner

This script runs all the inventory report tests and generates test data
for comprehensive testing of the inventory report functionality.
"""

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('inventory_report_tests.log')
    ]
)
logger = logging.getLogger(__name__)

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_command(command, description):
    """
    Run a shell command and log the output
    
    Args:
        command: Command to run as a list of strings
        description: Description of the command for logging
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    logger.info(f"Running {description}...")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return_code = process.returncode
        
        if return_code == 0:
            logger.info(f"{description} completed successfully")
        else:
            logger.error(f"{description} failed with return code {return_code}")
            logger.error(f"Error: {stderr}")
        
        return return_code, stdout, stderr
    except Exception as e:
        logger.error(f"Error running {description}: {e}")
        return -1, "", str(e)

def generate_test_data(sizes=["small", "medium", "large"]):
    """
    Generate test data for different inventory sizes
    
    Args:
        sizes: List of inventory sizes to generate
    """
    logger.info("Generating test data...")
    
    for size in sizes:
        output_file = f"inventory_test_data_{size}.json"
        command = [
            "python",
            "inventory_report_test_data_generator.py",
            f"--size={size}",
            f"--output={output_file}"
        ]
        
        return_code, stdout, stderr = run_command(
            command,
            f"Generating {size} inventory test data"
        )
        
        if return_code == 0:
            logger.info(f"Generated {size} inventory test data: {output_file}")

def run_nlp_tests():
    """
    Run NLP command recognition tests
    """
    logger.info("Running NLP command recognition tests...")
    
    command = ["python", "../nlp/test_get_inventory_report.py"]
    return_code, stdout, stderr = run_command(
        command,
        "NLP command recognition tests"
    )
    
    if return_code == 0:
        logger.info("NLP command recognition tests passed")
        print(stdout)
    else:
        logger.error("NLP command recognition tests failed")
        print(stderr)

def run_pdf_generation_tests():
    """
    Run PDF generation tests
    """
    logger.info("Running PDF generation tests...")
    
    command = ["python", "../routes/test_inventory_report_pdf.py"]
    return_code, stdout, stderr = run_command(
        command,
        "PDF generation tests"
    )
    
    if return_code == 0:
        logger.info("PDF generation tests passed")
        print(stdout)
    else:
        logger.error("PDF generation tests failed")
        print(stderr)

def open_test_plan():
    """
    Open the test plan in the default application
    """
    test_plan_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "inventory_report_test_plan.md"
    )
    
    if os.path.exists(test_plan_path):
        if sys.platform == "darwin":  # macOS
            subprocess.call(["open", test_plan_path])
        elif sys.platform == "win32":  # Windows
            os.startfile(test_plan_path)
        else:  # Linux
            subprocess.call(["xdg-open", test_plan_path])
        
        logger.info(f"Opened test plan: {test_plan_path}")
    else:
        logger.error(f"Test plan not found: {test_plan_path}")

def open_visual_checklist():
    """
    Open the visual checklist in the default application
    """
    checklist_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "inventory_report_visual_checklist.md"
    )
    
    if os.path.exists(checklist_path):
        if sys.platform == "darwin":  # macOS
            subprocess.call(["open", checklist_path])
        elif sys.platform == "win32":  # Windows
            os.startfile(checklist_path)
        else:  # Linux
            subprocess.call(["xdg-open", checklist_path])
        
        logger.info(f"Opened visual checklist: {checklist_path}")
    else:
        logger.error(f"Visual checklist not found: {checklist_path}")

def create_test_results_file():
    """
    Create a new test results file from the template
    """
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "inventory_report_test_results_template.md"
    )
    
    if not os.path.exists(template_path):
        logger.error(f"Test results template not found: {template_path}")
        return None
    
    # Create a new test results file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"inventory_report_test_results_{timestamp}.md"
    )
    
    # Copy template to new file
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    
    # Replace placeholders
    test_date = datetime.now().strftime("%Y-%m-%d")
    content = template_content.replace("[Date]", test_date)
    
    with open(results_path, "w") as results_file:
        results_file.write(content)
    
    logger.info(f"Created test results file: {results_path}")
    return results_path

def main():
    parser = argparse.ArgumentParser(description="Run inventory report tests")
    parser.add_argument(
        "--generate-data", action="store_true",
        help="Generate test data for different inventory sizes"
    )
    parser.add_argument(
        "--run-nlp-tests", action="store_true",
        help="Run NLP command recognition tests"
    )
    parser.add_argument(
        "--run-pdf-tests", action="store_true",
        help="Run PDF generation tests"
    )
    parser.add_argument(
        "--open-plan", action="store_true",
        help="Open the test plan"
    )
    parser.add_argument(
        "--open-checklist", action="store_true",
        help="Open the visual checklist"
    )
    parser.add_argument(
        "--create-results", action="store_true",
        help="Create a new test results file from the template"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all tests and open all documents"
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Run all if --all specified
    if args.all:
        args.generate_data = True
        args.run_nlp_tests = True
        args.run_pdf_tests = True
        args.open_plan = True
        args.open_checklist = True
        args.create_results = True
    
    # Run selected tests
    if args.generate_data:
        generate_test_data()
    
    if args.run_nlp_tests:
        run_nlp_tests()
    
    if args.run_pdf_tests:
        run_pdf_generation_tests()
    
    if args.open_plan:
        open_test_plan()
    
    if args.open_checklist:
        open_visual_checklist()
    
    if args.create_results:
        results_path = create_test_results_file()
        if results_path:
            # Open the results file
            if sys.platform == "darwin":  # macOS
                subprocess.call(["open", results_path])
            elif sys.platform == "win32":  # Windows
                os.startfile(results_path)
            else:  # Linux
                subprocess.call(["xdg-open", results_path])

if __name__ == "__main__":
    main()