#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Comprehensive Test Suite for Multilingual NLP System

This script provides a comprehensive testing framework for evaluating
the performance of the multilingual NLP system across different languages,
intents, and entity extraction capabilities.
"""

import json
import os
import time
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from datetime import datetime

# Import the NLP components
# Assuming these modules are available in the project
try:
    from enhanced_language_model import parse_multilingual_command, detect_language_with_confidence
    from chatbot_integration import ChatbotIntegration
except ImportError:
    print("Warning: Could not import NLP modules. Running in mock mode.")
    # Mock implementations for testing without actual modules
    def parse_multilingual_command(text):
        return {
            "language": "en",
            "is_mixed_language": False,
            "intent": "get_inventory",
            "confidence": 0.9,
            "entities": {}
        }
    
    def detect_language_with_confidence(text):
        return "en", 0.9
    
    class ChatbotIntegration:
        def process_message(self, message, user_id):
            return f"Processed: {message}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_suite.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("test_suite")

# Test data for different intents and languages
TEST_DATA = {
    "english": {
        "get_inventory": [
            "Show me my inventory",
            "What's in my inventory?",
            "List all my products",
            "Display my current stock",
            "What products do I have?"
        ],
        "get_low_stock": [
            "Show low stock items",
            "Which products are running low?",
            "List products with low inventory",
            "Display items that need restocking",
            "What's running out of stock?"
        ],
        "get_report": [
            "Generate sales report for last week",
            "Show me the report for this month",
            "Get sales data for January",
            "I need a report for Q1",
            "Show performance report for last 30 days"
        ],
        "edit_stock": [
            "Update rice stock to 50 kg",
            "Change sugar inventory to 100 packets",
            "Set wheat quantity to 75 kg",
            "Modify dal stock to 30 kg",
            "Update oil inventory to 45 liters"
        ],
        "get_orders": [
            "Show my recent orders",
            "Display orders from last week",
            "List all pending orders",
            "Get completed orders for this month",
            "Show orders from January 1st"
        ],
        "search_product": [
            "Search for rice products",
            "Find items with sugar",
            "Look up wheat flour",
            "Search inventory for dal",
            "Find products with oil"
        ]
    },
    "hindi": {
        "get_inventory": [
            "मेरा इन्वेंटरी दिखाओ",
            "मेरे पास क्या स्टॉक है?",
            "सभी प्रोडक्ट्स की लिस्ट दिखाओ",
            "वर्तमान स्टॉक दिखाएं",
            "मेरे पास कौन से प्रोडक्ट्स हैं?"
        ],
        "get_low_stock": [
            "कम स्टॉक वाले आइटम दिखाओ",
            "कौन से प्रोडक्ट्स कम हो रहे हैं?",
            "कम इन्वेंटरी वाले प्रोडक्ट्स की सूची",
            "वे आइटम दिखाएं जिन्हें रीस्टॉक करने की आवश्यकता है",
            "क्या स्टॉक से बाहर हो रहा है?"
        ],
        "get_report": [
            "पिछले हफ्ते की बिक्री रिपोर्ट जनरेट करें",
            "इस महीने की रिपोर्ट दिखाएं",
            "जनवरी के लिए सेल्स डेटा प्राप्त करें",
            "मुझे Q1 के लिए एक रिपोर्ट चाहिए",
            "पिछले 30 दिनों के लिए परफॉरमेंस रिपोर्ट दिखाएं"
        ],
        "edit_stock": [
            "चावल का स्टॉक 50 किलो अपडेट करें",
            "चीनी इन्वेंटरी को 100 पैकेट में बदलें",
            "गेहूं की मात्रा 75 किलो सेट करें",
            "दाल स्टॉक को 30 किलो में संशोधित करें",
            "तेल इन्वेंटरी को 45 लीटर अपडेट करें"
        ],
        "get_orders": [
            "मेरे हाल के ऑर्डर दिखाएं",
            "पिछले हफ्ते के ऑर्डर दिखाएं",
            "सभी लंबित ऑर्डर सूचीबद्ध करें",
            "इस महीने के पूरे ऑर्डर प्राप्त करें",
            "1 जनवरी से ऑर्डर दिखाएं"
        ],
        "search_product": [
            "चावल प्रोडक्ट्स के लिए खोजें",
            "चीनी वाले आइटम खोजें",
            "गेहूं का आटा देखें",
            "दाल के लिए इन्वेंटरी खोजें",
            "तेल वाले प्रोडक्ट्स खोजें"
        ]
    },
    "mixed": {
        "get_inventory": [
            "Show मेरा inventory",
            "What's मेरे पास in stock?",
            "List सभी products",
            "Display वर्तमान stock",
            "What प्रोडक्ट्स do I have?"
        ],
        "get_low_stock": [
            "Show कम stock items",
            "Which प्रोडक्ट्स are running low?",
            "List कम inventory वाले products",
            "Display items that need रीस्टॉक",
            "What's स्टॉक से बाहर हो रहा है?"
        ],
        "get_report": [
            "Generate पिछले हफ्ते की sales report",
            "Show me the रिपोर्ट for this month",
            "Get जनवरी के लिए sales data",
            "I need a Q1 के लिए report",
            "Show पिछले 30 दिनों के लिए performance report"
        ],
        "edit_stock": [
            "Update चावल stock to 50 kg",
            "Change चीनी inventory to 100 packets",
            "Set गेहूं quantity to 75 kg",
            "Modify दाल stock to 30 kg",
            "Update तेल inventory to 45 liters"
        ],
        "get_orders": [
            "Show मेरे हाल के orders",
            "Display पिछले हफ्ते के orders",
            "List all लंबित orders",
            "Get इस महीने के completed orders",
            "Show 1 जनवरी से orders"
        ],
        "search_product": [
            "Search for चावल products",
            "Find चीनी वाले items",
            "Look up गेहूं का आटा",
            "Search inventory for दाल",
            "Find तेल वाले products"
        ]
    }
}

# Expected intents and entities for test validation
EXPECTED_RESULTS = {
    "english": {
        "get_inventory": {"intent": "get_inventory", "entities": {}},
        "get_low_stock": {"intent": "get_low_stock", "entities": {}},
        "get_report": {"intent": "get_report", "entities": {"time_period": "last_week"}},
        "edit_stock": {"intent": "edit_stock", "entities": {"product_name": "rice", "stock": 50}},
        "get_orders": {"intent": "get_orders", "entities": {"time_period": "recent"}},
        "search_product": {"intent": "search_product", "entities": {"product_name": "rice"}}
    },
    "hindi": {
        "get_inventory": {"intent": "get_inventory", "entities": {}},
        "get_low_stock": {"intent": "get_low_stock", "entities": {}},
        "get_report": {"intent": "get_report", "entities": {"time_period": "last_week"}},
        "edit_stock": {"intent": "edit_stock", "entities": {"product_name": "चावल", "stock": 50}},
        "get_orders": {"intent": "get_orders", "entities": {"time_period": "recent"}},
        "search_product": {"intent": "search_product", "entities": {"product_name": "चावल"}}
    },
    "mixed": {
        "get_inventory": {"intent": "get_inventory", "entities": {}},
        "get_low_stock": {"intent": "get_low_stock", "entities": {}},
        "get_report": {"intent": "get_report", "entities": {"time_period": "last_week"}},
        "edit_stock": {"intent": "edit_stock", "entities": {"product_name": "चावल", "stock": 50}},
        "get_orders": {"intent": "get_orders", "entities": {"time_period": "recent"}},
        "search_product": {"intent": "search_product", "entities": {"product_name": "चावल"}}
    }
}

# Language detection test data
LANGUAGE_TEST_DATA = {
    "en": [
        "Show me my inventory",
        "Update rice stock to 50 kg",
        "Generate sales report for last week",
        "What products are running low on stock?",
        "Search for wheat flour in my inventory"
    ],
    "hi": [
        "मेरा इन्वेंटरी दिखाओ",
        "चावल का स्टॉक 50 किलो अपडेट करें",
        "पिछले हफ्ते की बिक्री रिपोर्ट जनरेट करें",
        "कौन से प्रोडक्ट्स कम स्टॉक में हैं?",
        "मेरे इन्वेंटरी में गेहूं का आटा खोजें"
    ],
    "mixed": [
        "Show मेरा inventory",
        "Update चावल stock to 50 kg",
        "Generate पिछले हफ्ते की sales report",
        "Which प्रोडक्ट्स are low on stock?",
        "Search for गेहूं का आटा in my inventory"
    ]
}

# Edge cases for testing robustness
EDGE_CASES = [
    # Empty input
    "",
    # Very short input
    "hi",
    # Very long input
    "I need to update the stock of rice to 50 kg and also check if wheat flour is running low and then generate a sales report for the last month and also search for all products containing sugar and finally show me all pending orders from last week",
    # Special characters
    "Update rice stock to 50 kg @#$%^",
    # Misspellings
    "Updaet rice stok to 50 kg",
    # Mixed script with numbers
    "चावल का stock 50kg update करें",
    # Ambiguous intent
    "Show products",
    # Multiple intents
    "Update rice stock and show orders"
]

class TestSuite:
    """Comprehensive test suite for evaluating the multilingual NLP system."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.results = {
            "language_detection": [],
            "intent_recognition": [],
            "entity_extraction": [],
            "end_to_end": [],
            "edge_cases": []
        }
        self.chatbot = ChatbotIntegration()
        self.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create results directory if it doesn't exist
        os.makedirs("test_results", exist_ok=True)
    
    def test_language_detection(self):
        """Test language detection accuracy."""
        logger.info("Testing language detection...")
        results = []
        
        for expected_lang, texts in LANGUAGE_TEST_DATA.items():
            for text in texts:
                start_time = time.time()
                detected_lang, confidence = detect_language_with_confidence(text)
                processing_time = time.time() - start_time
                
                is_correct = False
                if expected_lang == "mixed" and detected_lang in ["mixed", "en_hi", "hi_en"]:
                    is_correct = True
                elif expected_lang == detected_lang:
                    is_correct = True
                
                result = {
                    "text": text,
                    "expected_language": expected_lang,
                    "detected_language": detected_lang,
                    "confidence": confidence,
                    "is_correct": is_correct,
                    "processing_time": processing_time
                }
                results.append(result)
                logger.debug(f"Language detection: {text} -> {detected_lang} (Expected: {expected_lang})")
        
        self.results["language_detection"] = results
        accuracy = sum(1 for r in results if r["is_correct"]) / len(results)
        logger.info(f"Language detection accuracy: {accuracy:.2f}")
        return accuracy
    
    def test_intent_recognition(self):
        """Test intent recognition accuracy across languages."""
        logger.info("Testing intent recognition...")
        results = []
        
        for language, intents in TEST_DATA.items():
            for expected_intent, texts in intents.items():
                for text in texts:
                    start_time = time.time()
                    parsed = parse_multilingual_command(text)
                    processing_time = time.time() - start_time
                    
                    detected_intent = parsed.get("intent", "")
                    confidence = parsed.get("confidence", 0)
                    is_correct = detected_intent == expected_intent
                    
                    result = {
                        "text": text,
                        "language": language,
                        "expected_intent": expected_intent,
                        "detected_intent": detected_intent,
                        "confidence": confidence,
                        "is_correct": is_correct,
                        "processing_time": processing_time
                    }
                    results.append(result)
                    logger.debug(f"Intent recognition: {text} -> {detected_intent} (Expected: {expected_intent})")
        
        self.results["intent_recognition"] = results
        accuracy = sum(1 for r in results if r["is_correct"]) / len(results)
        logger.info(f"Intent recognition accuracy: {accuracy:.2f}")
        return accuracy
    
    def test_entity_extraction(self):
        """Test entity extraction accuracy."""
        logger.info("Testing entity extraction...")
        results = []
        
        for language, intents in TEST_DATA.items():
            for intent_name, texts in intents.items():
                expected_entities = EXPECTED_RESULTS[language][intent_name]["entities"]
                
                for text in texts:
                    start_time = time.time()
                    parsed = parse_multilingual_command(text)
                    processing_time = time.time() - start_time
                    
                    extracted_entities = parsed.get("entities", {})
                    
                    # Check if all expected entities are present
                    all_entities_present = True
                    for key, value in expected_entities.items():
                        if key not in extracted_entities:
                            all_entities_present = False
                            break
                    
                    result = {
                        "text": text,
                        "language": language,
                        "intent": intent_name,
                        "expected_entities": expected_entities,
                        "extracted_entities": extracted_entities,
                        "all_entities_present": all_entities_present,
                        "processing_time": processing_time
                    }
                    results.append(result)
                    logger.debug(f"Entity extraction: {text} -> {extracted_entities}")
        
        self.results["entity_extraction"] = results
        accuracy = sum(1 for r in results if r["all_entities_present"]) / len(results)
        logger.info(f"Entity extraction accuracy: {accuracy:.2f}")
        return accuracy
    
    def test_end_to_end(self):
        """Test end-to-end processing with the chatbot integration."""
        logger.info("Testing end-to-end processing...")
        results = []
        
        for language, intents in TEST_DATA.items():
            for intent_name, texts in intents.items():
                for text in texts:
                    start_time = time.time()
                    response = self.chatbot.process_message(text, "test_user")
                    processing_time = time.time() - start_time
                    
                    # For end-to-end testing, we just check if a response was generated
                    has_response = bool(response)
                    
                    result = {
                        "text": text,
                        "language": language,
                        "intent": intent_name,
                        "response": response,
                        "has_response": has_response,
                        "processing_time": processing_time
                    }
                    results.append(result)
                    logger.debug(f"End-to-end: {text} -> Response generated: {has_response}")
        
        self.results["end_to_end"] = results
        success_rate = sum(1 for r in results if r["has_response"]) / len(results)
        logger.info(f"End-to-end success rate: {success_rate:.2f}")
        return success_rate
    
    def test_edge_cases(self):
        """Test system robustness with edge cases."""
        logger.info("Testing edge cases...")
        results = []
        
        for text in EDGE_CASES:
            try:
                start_time = time.time()
                parsed = parse_multilingual_command(text)
                processing_time = time.time() - start_time
                
                # For edge cases, we're mainly checking if the system handles them without errors
                result = {
                    "text": text,
                    "parsed_successfully": True,
                    "result": parsed,
                    "processing_time": processing_time,
                    "error": None
                }
            except Exception as e:
                result = {
                    "text": text,
                    "parsed_successfully": False,
                    "result": None,
                    "processing_time": None,
                    "error": str(e)
                }
            
            results.append(result)
            logger.debug(f"Edge case: {text} -> Parsed successfully: {result['parsed_successfully']}")
        
        self.results["edge_cases"] = results
        robustness = sum(1 for r in results if r["parsed_successfully"]) / len(results)
        logger.info(f"Edge case robustness: {robustness:.2f}")
        return robustness
    
    def run_all_tests(self):
        """Run all tests in the test suite."""
        logger.info("Running all tests...")
        
        metrics = {
            "language_detection_accuracy": self.test_language_detection(),
            "intent_recognition_accuracy": self.test_intent_recognition(),
            "entity_extraction_accuracy": self.test_entity_extraction(),
            "end_to_end_success_rate": self.test_end_to_end(),
            "edge_case_robustness": self.test_edge_cases()
        }
        
        self.generate_reports(metrics)
        return metrics
    
    def generate_reports(self, metrics):
        """Generate test reports and visualizations."""
        logger.info("Generating test reports...")
        
        # Save detailed results
        results_file = f"test_results/detailed_results_{self.test_timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # Save metrics summary
        metrics_file = f"test_results/metrics_summary_{self.test_timestamp}.json"
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Generate confusion matrix for intent recognition
        self.generate_confusion_matrix()
        
        # Generate accuracy by language chart
        self.generate_accuracy_by_language()
        
        # Generate accuracy by intent chart
        self.generate_accuracy_by_intent()
        
        # Generate processing time analysis
        self.generate_processing_time_analysis()
        
        # Generate summary report
        self.generate_summary_report(metrics)
        
        logger.info(f"Reports generated in test_results/ directory")
    
    def generate_confusion_matrix(self):
        """Generate confusion matrix for intent recognition."""
        intent_results = self.results["intent_recognition"]
        
        if not intent_results:
            return
        
        # Extract true and predicted intents
        y_true = [r["expected_intent"] for r in intent_results]
        y_pred = [r["detected_intent"] for r in intent_results]
        
        # Get unique intents
        unique_intents = sorted(set(y_true))
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred, labels=unique_intents)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Intent Recognition Confusion Matrix')
        plt.colorbar()
        tick_marks = np.arange(len(unique_intents))
        plt.xticks(tick_marks, unique_intents, rotation=45)
        plt.yticks(tick_marks, unique_intents)
        
        # Add text annotations
        thresh = cm.max() / 2
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        plt.tight_layout()
        plt.ylabel('True Intent')
        plt.xlabel('Predicted Intent')
        
        # Save the figure
        plt.savefig(f"test_results/confusion_matrix_{self.test_timestamp}.png")
        plt.close()
    
    def generate_accuracy_by_language(self):
        """Generate chart showing accuracy by language."""
        intent_results = self.results["intent_recognition"]
        
        if not intent_results:
            return
        
        # Group by language and calculate accuracy
        language_accuracy = {}
        for language in ["english", "hindi", "mixed"]:
            language_results = [r for r in intent_results if r["language"] == language]
            if language_results:
                accuracy = sum(1 for r in language_results if r["is_correct"]) / len(language_results)
                language_accuracy[language] = accuracy
        
        # Plot accuracy by language
        plt.figure(figsize=(10, 6))
        languages = list(language_accuracy.keys())
        accuracies = list(language_accuracy.values())
        
        plt.bar(languages, accuracies, color=['blue', 'green', 'orange'])
        plt.title('Intent Recognition Accuracy by Language')
        plt.xlabel('Language')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)
        
        # Add text labels
        for i, v in enumerate(accuracies):
            plt.text(i, v + 0.02, f"{v:.2f}", ha='center')
        
        # Save the figure
        plt.savefig(f"test_results/accuracy_by_language_{self.test_timestamp}.png")
        plt.close()
    
    def generate_accuracy_by_intent(self):
        """Generate chart showing accuracy by intent."""
        intent_results = self.results["intent_recognition"]
        
        if not intent_results:
            return
        
        # Group by intent and calculate accuracy
        intent_accuracy = {}
        for intent in ["get_inventory", "get_low_stock", "get_report", "edit_stock", "get_orders", "search_product"]:
            intent_results_filtered = [r for r in intent_results if r["expected_intent"] == intent]
            if intent_results_filtered:
                accuracy = sum(1 for r in intent_results_filtered if r["is_correct"]) / len(intent_results_filtered)
                intent_accuracy[intent] = accuracy
        
        # Plot accuracy by intent
        plt.figure(figsize=(12, 6))
        intents = list(intent_accuracy.keys())
        accuracies = list(intent_accuracy.values())
        
        plt.bar(intents, accuracies, color='skyblue')
        plt.title('Intent Recognition Accuracy by Intent')
        plt.xlabel('Intent')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        
        # Add text labels
        for i, v in enumerate(accuracies):
            plt.text(i, v + 0.02, f"{v:.2f}", ha='center')
        
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(f"test_results/accuracy_by_intent_{self.test_timestamp}.png")
        plt.close()
    
    def generate_processing_time_analysis(self):
        """Generate processing time analysis charts."""
        # Collect processing times from different test types
        processing_times = {
            "Language Detection": [r["processing_time"] for r in self.results["language_detection"] if "processing_time" in r],
            "Intent Recognition": [r["processing_time"] for r in self.results["intent_recognition"] if "processing_time" in r],
            "Entity Extraction": [r["processing_time"] for r in self.results["entity_extraction"] if "processing_time" in r],
            "End-to-End": [r["processing_time"] for r in self.results["end_to_end"] if "processing_time" in r]
        }
        
        # Filter out empty lists
        processing_times = {k: v for k, v in processing_times.items() if v}
        
        if not processing_times:
            return
        
        # Plot processing time boxplot
        plt.figure(figsize=(12, 6))
        plt.boxplot([times for times in processing_times.values()], labels=list(processing_times.keys()))
        plt.title('Processing Time Analysis')
        plt.ylabel('Time (seconds)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Save the figure
        plt.savefig(f"test_results/processing_time_{self.test_timestamp}.png")
        plt.close()
        
        # Calculate and save processing time statistics
        stats = {}
        for name, times in processing_times.items():
            stats[name] = {
                "mean": np.mean(times),
                "median": np.median(times),
                "min": np.min(times),
                "max": np.max(times),
                "std": np.std(times)
            }
        
        with open(f"test_results/processing_time_stats_{self.test_timestamp}.json", 'w') as f:
            json.dump(stats, f, indent=2)
    
    def generate_summary_report(self, metrics):
        """Generate a summary report in Markdown format."""
        report = f"# Multilingual NLP System Test Report\n\n"
        report += f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "## Performance Metrics\n\n"
        report += "| Metric | Value |\n"
        report += "|--------|-------|\n"
        for name, value in metrics.items():
            report += f"| {name.replace('_', ' ').title()} | {value:.2f} |\n"
        
        report += "\n## Test Coverage\n\n"
        report += f"- **Languages tested:** English, Hindi, Mixed\n"
        report += f"- **Intents tested:** {', '.join(TEST_DATA['english'].keys())}\n"
        report += f"- **Total test cases:** {sum(len(tests) for lang in TEST_DATA.values() for tests in lang.values())}\n"
        report += f"- **Edge cases tested:** {len(EDGE_CASES)}\n"
        
        report += "\n## Key Findings\n\n"
        
        # Language detection findings
        lang_results = self.results["language_detection"]
        if lang_results:
            correct = sum(1 for r in lang_results if r["is_correct"])
            total = len(lang_results)
            report += f"### Language Detection\n\n"
            report += f"- **Accuracy:** {correct}/{total} ({correct/total:.2%})\n"
            
            # Find problematic cases
            incorrect = [r for r in lang_results if not r["is_correct"]]
            if incorrect:
                report += "- **Problematic cases:**\n"
                for case in incorrect[:3]:  # Show up to 3 examples
                    report += f"  - Text: '{case['text']}' - Expected: {case['expected_language']}, Detected: {case['detected_language']}\n"
        
        # Intent recognition findings
        intent_results = self.results["intent_recognition"]
        if intent_results:
            correct = sum(1 for r in intent_results if r["is_correct"])
            total = len(intent_results)
            report += f"\n### Intent Recognition\n\n"
            report += f"- **Accuracy:** {correct}/{total} ({correct/total:.2%})\n"
            
            # Accuracy by language
            report += "- **Accuracy by language:**\n"
            for language in ["english", "hindi", "mixed"]:
                lang_results = [r for r in intent_results if r["language"] == language]
                if lang_results:
                    lang_correct = sum(1 for r in lang_results if r["is_correct"])
                    lang_total = len(lang_results)
                    report += f"  - {language.title()}: {lang_correct}/{lang_total} ({lang_correct/lang_total:.2%})\n"
            
            # Find problematic intents
            intent_accuracy = {}
            for intent in set(r["expected_intent"] for r in intent_results):
                intent_results_filtered = [r for r in intent_results if r["expected_intent"] == intent]
                if intent_results_filtered:
                    accuracy = sum(1 for r in intent_results_filtered if r["is_correct"]) / len(intent_results_filtered)
                    intent_accuracy[intent] = accuracy
            
            problematic_intents = [intent for intent, acc in intent_accuracy.items() if acc < 0.8]
            if problematic_intents:
                report += "- **Intents needing improvement:**\n"
                for intent in problematic_intents:
                    report += f"  - {intent}: {intent_accuracy[intent]:.2%} accuracy\n"
        
        # Entity extraction findings
        entity_results = self.results["entity_extraction"]
        if entity_results:
            correct = sum(1 for r in entity_results if r["all_entities_present"])
            total = len(entity_results)
            report += f"\n### Entity Extraction\n\n"
            report += f"- **Accuracy:** {correct}/{total} ({correct/total:.2%})\n"
            
            # Find problematic entity types
            problematic_cases = [r for r in entity_results if not r["all_entities_present"]]
            if problematic_cases:
                report += "- **Problematic entity types:**\n"
                entity_issues = {}
                for case in problematic_cases:
                    intent = case["intent"]
                    if intent not in entity_issues:
                        entity_issues[intent] = 0
                    entity_issues[intent] += 1
                
                for intent, count in entity_issues.items():
                    report += f"  - {intent}: {count} issues\n"
        
        # Edge case findings
        edge_results = self.results["edge_cases"]
        if edge_results:
            successful = sum(1 for r in edge_results if r["parsed_successfully"])
            total = len(edge_results)
            report += f"\n### Edge Cases\n\n"
            report += f"- **Success rate:** {successful}/{total} ({successful/total:.2%})\n"
            
            # Find failed edge cases
            failed = [r for r in edge_results if not r["parsed_successfully"]]
            if failed:
                report += "- **Failed edge cases:**\n"
                for case in failed:
                    report += f"  - Text: '{case['text']}' - Error: {case['error']}\n"
        
        report += "\n## Recommendations\n\n"
        
        # Add recommendations based on test results
        recommendations = []
        
        # Language detection recommendations
        lang_accuracy = metrics.get("language_detection_accuracy", 0)
        if lang_accuracy < 0.9:
            recommendations.append("Improve language detection accuracy, especially for mixed language inputs.")
        
        # Intent recognition recommendations
        intent_accuracy = metrics.get("intent_recognition_accuracy", 0)
        if intent_accuracy < 0.9:
            recommendations.append("Enhance intent recognition patterns, particularly for problematic intents.")
        
        # Entity extraction recommendations
        entity_accuracy = metrics.get("entity_extraction_accuracy", 0)
        if entity_accuracy < 0.9:
            recommendations.append("Refine entity extraction rules to improve accuracy.")
        
        # Edge case recommendations
        edge_robustness = metrics.get("edge_case_robustness", 0)
        if edge_robustness < 0.9:
            recommendations.append("Improve system robustness for handling edge cases.")
        
        # Add general recommendations
        recommendations.extend([
            "Continuously update training data with real user queries.",
            "Consider implementing a feedback loop to capture and learn from misclassifications.",
            "Regularly evaluate system performance as new features are added."
        ])
        
        for i, recommendation in enumerate(recommendations, 1):
            report += f"{i}. {recommendation}\n"
        
        report += "\n## Visualizations\n\n"
        report += f"- [Confusion Matrix](confusion_matrix_{self.test_timestamp}.png)\n"
        report += f"- [Accuracy by Language](accuracy_by_language_{self.test_timestamp}.png)\n"
        report += f"- [Accuracy by Intent](accuracy_by_intent_{self.test_timestamp}.png)\n"
        report += f"- [Processing Time Analysis](processing_time_{self.test_timestamp}.png)\n"
        
        # Save the report
        with open(f"test_results/summary_report_{self.test_timestamp}.md", 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    """Run the test suite."""
    print("Starting Multilingual NLP System Test Suite")
    test_suite = TestSuite()
    metrics = test_suite.run_all_tests()
    
    print("\nTest Results Summary:")
    for name, value in metrics.items():
        print(f"{name.replace('_', ' ').title()}: {value:.2f}")
    
    print(f"\nDetailed reports saved in test_results/ directory")


if __name__ == "__main__":
    main()