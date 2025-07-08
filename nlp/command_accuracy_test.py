import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

class CommandAccuracyTest:
    def __init__(self):
        self.results = {
            "edit_stock": {"en": {"pass": 0, "fail": 0}, "hi": {"pass": 0, "fail": 0}},
            "get_orders": {"en": {"pass": 0, "fail": 0}, "hi": {"pass": 0, "fail": 0}},
            "get_report": {"en": {"pass": 0, "fail": 0}, "hi": {"pass": 0, "fail": 0}},
            "get_low_stock": {"en": {"pass": 0, "fail": 0}, "hi": {"pass": 0, "fail": 0}},
            "search_product": {"en": {"pass": 0, "fail": 0}, "hi": {"pass": 0, "fail": 0}}
        }
        self.parsed_examples = {
            "en": {},
            "hi": {}
        }
        self.routing_confirmation = {
            "edit_stock": False,
            "get_orders": False,
            "get_report": False,
            "get_low_stock": False,
            "search_product": False
        }
    
    def record_result(self, intent, language, success):
        if success:
            self.results[intent][language]["pass"] += 1
        else:
            self.results[intent][language]["fail"] += 1
    
    def record_parsed_example(self, intent, language, parsed_result):
        if intent not in self.parsed_examples[language]:
            self.parsed_examples[language][intent] = parsed_result
    
    def record_routing_confirmation(self, intent):
        self.routing_confirmation[intent] = True
    
    def test_edit_stock(self):
        print("\nTesting edit_stock command...")
        
        # English tests
        english_commands = [
            "Update stock of Sugar to 15",
            "Change Rice quantity to 20",
            "Set Tea stock to 30 units",
            "Make Salt inventory 25"
        ]
        
        for command in english_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "edit_stock" and \
                          parsed_result["language"] == "en" and \
                          "name" in parsed_result["entities"] and \
                          "quantity" in parsed_result["entities"]
                
                self.record_result("edit_stock", "en", success)
                
                if success and "edit_stock" not in self.parsed_examples["en"]:
                    self.record_parsed_example("edit_stock", "en", parsed_result)
                    
                    # Test routing with mock
                    with patch("nlp.command_router.make_api_request") as mock_api:
                        mock_api.return_value = {
                            "success": True,
                            "message": f"Updated {parsed_result['entities']['name']} stock to {parsed_result['entities']['quantity']}"
                        }
                        response = route_command(parsed_result)
                        if "updated" in response.lower() and parsed_result['entities']['name'].lower() in response.lower():
                            self.record_routing_confirmation("edit_stock")
                
                print(f"  EN - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  EN - '{command}': ✗ (Error: {str(e)})")
                self.record_result("edit_stock", "en", False)
        
        # Hindi tests
        hindi_commands = [
            "चीनी का स्टॉक 15 करो",
            "चावल की मात्रा 20 सेट करें",
            "चाय का स्टॉक 30 यूनिट करो",
            "नमक का इन्वेंटरी 25 बनाओ"
        ]
        
        for command in hindi_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "edit_stock" and \
                          parsed_result["language"] == "hi" and \
                          "name" in parsed_result["entities"] and \
                          "quantity" in parsed_result["entities"]
                
                self.record_result("edit_stock", "hi", success)
                
                if success and "edit_stock" not in self.parsed_examples["hi"]:
                    self.record_parsed_example("edit_stock", "hi", parsed_result)
                
                print(f"  HI - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  HI - '{command}': ✗ (Error: {str(e)})")
                self.record_result("edit_stock", "hi", False)
    
    def test_get_orders(self):
        print("\nTesting get_orders command...")
        
        # English tests
        english_commands = [
            "Show all orders",
            "Get orders from last week",
            "Show pending orders",
            "Get orders from yesterday with status delivered"
        ]
        
        for command in english_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_orders" and \
                          parsed_result["language"] == "en"
                
                self.record_result("get_orders", "en", success)
                
                if success and "get_orders" not in self.parsed_examples["en"]:
                    self.record_parsed_example("get_orders", "en", parsed_result)
                    
                    # Test routing with mock
                    with patch("nlp.command_router.make_api_request") as mock_api:
                        mock_api.return_value = {
                            "success": True,
                            "orders": [
                                {"id": 1, "customer": "John", "items": ["Sugar", "Tea"], "status": "pending"},
                                {"id": 2, "customer": "Mary", "items": ["Rice"], "status": "delivered"}
                            ]
                        }
                        response = route_command(parsed_result)
                        if "orders" in response.lower():
                            self.record_routing_confirmation("get_orders")
                
                print(f"  EN - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  EN - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_orders", "en", False)
        
        # Hindi tests
        hindi_commands = [
            "सभी ऑर्डर दिखाओ",
            "पिछले हफ्ते के ऑर्डर दिखाओ",
            "लंबित ऑर्डर दिखाओ",
            "कल के डिलीवर्ड ऑर्डर दिखाओ"
        ]
        
        for command in hindi_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_orders" and \
                          parsed_result["language"] == "hi"
                
                self.record_result("get_orders", "hi", success)
                
                if success and "get_orders" not in self.parsed_examples["hi"]:
                    self.record_parsed_example("get_orders", "hi", parsed_result)
                
                print(f"  HI - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  HI - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_orders", "hi", False)
    
    def test_get_report(self):
        print("\nTesting get_report command...")
        
        # English tests
        english_commands = [
            "Show sales report",
            "Get report for today",
            "Show me last week's report",
            "Generate monthly sales report"
        ]
        
        for command in english_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_report" and \
                          parsed_result["language"] == "en"
                
                self.record_result("get_report", "en", success)
                
                if success and "get_report" not in self.parsed_examples["en"]:
                    self.record_parsed_example("get_report", "en", parsed_result)
                    
                    # Test routing with mock
                    with patch("nlp.command_router.make_api_request") as mock_api:
                        mock_api.return_value = {
                            "success": True,
                            "report": {
                                "total_sales": 5000,
                                "items_sold": 120,
                                "period": "today"
                            }
                        }
                        response = route_command(parsed_result)
                        if "report" in response.lower() and "sales" in response.lower():
                            self.record_routing_confirmation("get_report")
                
                print(f"  EN - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  EN - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_report", "en", False)
        
        # Hindi tests
        hindi_commands = [
            "बिक्री रिपोर्ट दिखाओ",
            "आज की रिपोर्ट दिखाओ",
            "पिछले हफ्ते की रिपोर्ट दिखाओ",
            "मासिक बिक्री रिपोर्ट बनाओ"
        ]
        
        for command in hindi_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_report" and \
                          parsed_result["language"] == "hi"
                
                self.record_result("get_report", "hi", success)
                
                if success and "get_report" not in self.parsed_examples["hi"]:
                    self.record_parsed_example("get_report", "hi", parsed_result)
                
                print(f"  HI - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  HI - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_report", "hi", False)
    
    def test_get_low_stock(self):
        print("\nTesting get_low_stock command...")
        
        # English tests
        english_commands = [
            "Show low stock items",
            "Display products with low inventory",
            "Which items are running low?",
            "Show items with stock below 10"
        ]
        
        for command in english_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_low_stock" and \
                          parsed_result["language"] == "en"
                
                self.record_result("get_low_stock", "en", success)
                
                if success and "get_low_stock" not in self.parsed_examples["en"]:
                    self.record_parsed_example("get_low_stock", "en", parsed_result)
                    
                    # Test routing with mock
                    with patch("nlp.command_router.make_api_request") as mock_api:
                        mock_api.return_value = {
                            "success": True,
                            "products": [
                                {"name": "Salt", "price": 20, "stock": 3},
                                {"name": "Tea", "price": 120, "stock": 4}
                            ]
                        }
                        response = route_command(parsed_result)
                        if "low stock" in response.lower():
                            self.record_routing_confirmation("get_low_stock")
                
                print(f"  EN - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  EN - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_low_stock", "en", False)
        
        # Hindi tests
        hindi_commands = [
            "कम स्टॉक दिखाओ",
            "कम इन्वेंटरी वाले प्रोडक्ट दिखाओ",
            "कौन से आइटम कम हो रहे हैं?",
            "10 से कम स्टॉक वाले आइटम दिखाओ"
        ]
        
        for command in hindi_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "get_low_stock" and \
                          parsed_result["language"] == "hi"
                
                self.record_result("get_low_stock", "hi", success)
                
                if success and "get_low_stock" not in self.parsed_examples["hi"]:
                    self.record_parsed_example("get_low_stock", "hi", parsed_result)
                
                print(f"  HI - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  HI - '{command}': ✗ (Error: {str(e)})")
                self.record_result("get_low_stock", "hi", False)
    
    def test_search_product(self):
        print("\nTesting search_product command...")
        
        # English tests
        english_commands = [
            "Search for sugar",
            "Do you have rice in stock?",
            "Is salt available?",
            "Find tea in inventory"
        ]
        
        for command in english_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "search_product" and \
                          parsed_result["language"] == "en" and \
                          "name" in parsed_result["entities"]
                
                self.record_result("search_product", "en", success)
                
                if success and "search_product" not in self.parsed_examples["en"]:
                    self.record_parsed_example("search_product", "en", parsed_result)
                    
                    # Test routing with mock
                    with patch("nlp.command_router.make_api_request") as mock_api:
                        mock_api.return_value = {
                            "success": True,
                            "found": True,
                            "name": parsed_result["entities"]["name"],
                            "stock": 15,
                            "price": 40
                        }
                        response = route_command(parsed_result)
                        if "available" in response.lower():
                            self.record_routing_confirmation("search_product")
                
                print(f"  EN - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  EN - '{command}': ✗ (Error: {str(e)})")
                self.record_result("search_product", "en", False)
        
        # Hindi tests
        hindi_commands = [
            "चीनी सर्च करो",
            "क्या चावल स्टॉक में है?",
            "नमक उपलब्ध है क्या?",
            "चाय इन्वेंटरी में खोजो"
        ]
        
        for command in hindi_commands:
            try:
                parsed_result = parse_multilingual_command(command)
                success = parsed_result["intent"] == "search_product" and \
                          parsed_result["language"] == "hi" and \
                          "name" in parsed_result["entities"]
                
                self.record_result("search_product", "hi", success)
                
                if success and "search_product" not in self.parsed_examples["hi"]:
                    self.record_parsed_example("search_product", "hi", parsed_result)
                
                print(f"  HI - '{command}': {'✓' if success else '✗'}")
            except Exception as e:
                print(f"  HI - '{command}': ✗ (Error: {str(e)})")
                self.record_result("search_product", "hi", False)
    
    def run_all_tests(self):
        print("Starting NLP Command Accuracy Tests...\n")
        self.test_edit_stock()
        self.test_get_orders()
        self.test_get_report()
        self.test_get_low_stock()
        self.test_search_product()
        
        self.print_results()
        
        # Save results to file
        self.save_results_to_file()
    
    def print_results(self):
        print("\n" + "=" * 60)
        print("NLP COMMAND RESPONSE ACCURACY MATRIX")
        print("=" * 60)
        print(f"{'Command':<15} | {'English':<20} | {'Hindi':<20}")
        print("-" * 60)
        
        for intent in self.results:
            en_pass = self.results[intent]["en"]["pass"]
            en_total = en_pass + self.results[intent]["en"]["fail"]
            en_rate = (en_pass / en_total * 100) if en_total > 0 else 0
            
            hi_pass = self.results[intent]["hi"]["pass"]
            hi_total = hi_pass + self.results[intent]["hi"]["fail"]
            hi_rate = (hi_pass / hi_total * 100) if hi_total > 0 else 0
            
            print(f"{intent:<15} | {en_pass}/{en_total} ({en_rate:.1f}%) {' PASS' if en_rate == 100 else ' FAIL':<5} | {hi_pass}/{hi_total} ({hi_rate:.1f}%) {' PASS' if hi_rate == 100 else ' FAIL':<5}")
        
        print("\n" + "=" * 60)
        print("PARSED OUTPUT EXAMPLES")
        print("=" * 60)
        
        print("\nENGLISH EXAMPLES:")
        for intent, parsed in self.parsed_examples["en"].items():
            print(f"\n{intent.upper()}:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        
        print("\nHINDI EXAMPLES:")
        for intent, parsed in self.parsed_examples["hi"].items():
            print(f"\n{intent.upper()}:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 60)
        print("INTENT ROUTING CONFIRMATION")
        print("=" * 60)
        
        for intent, confirmed in self.routing_confirmation.items():
            print(f"{intent:<15}: {'✓ Confirmed' if confirmed else '✗ Not confirmed'}")
    
    def save_results_to_file(self):
        # Create results dictionary
        results_data = {
            "accuracy_matrix": {},
            "parsed_examples": self.parsed_examples,
            "routing_confirmation": {}
        }
        
        # Format accuracy matrix
        for intent in self.results:
            en_pass = self.results[intent]["en"]["pass"]
            en_total = en_pass + self.results[intent]["en"]["fail"]
            en_rate = (en_pass / en_total * 100) if en_total > 0 else 0
            
            hi_pass = self.results[intent]["hi"]["pass"]
            hi_total = hi_pass + self.results[intent]["hi"]["fail"]
            hi_rate = (hi_pass / hi_total * 100) if hi_total > 0 else 0
            
            results_data["accuracy_matrix"][intent] = {
                "en": {
                    "pass": en_pass,
                    "total": en_total,
                    "rate": en_rate,
                    "status": "PASS" if en_rate == 100 else "FAIL"
                },
                "hi": {
                    "pass": hi_pass,
                    "total": hi_total,
                    "rate": hi_rate,
                    "status": "PASS" if hi_rate == 100 else "FAIL"
                }
            }
        
        # Format routing confirmation
        for intent, confirmed in self.routing_confirmation.items():
            results_data["routing_confirmation"][intent] = confirmed
        
        # Save to file
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.json"), "w", encoding="utf-8") as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    tester = CommandAccuracyTest()
    tester.run_all_tests()