#!/usr/bin/env python3
"""
Model Evaluation for Multilingual NLP Model

This script evaluates the performance of the enhanced language model
across different languages (English, Hindi, and mixed) and intents.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from datetime import datetime

# Import the enhanced language model
from enhanced_language_model import parse_multilingual_command, recognize_intent

def load_test_data(file_path="./data/testing_data.json"):
    """Load test data from JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Test data file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []

def evaluate_model(test_data):
    """Evaluate model performance on test data"""
    results = []
    true_intents = []
    pred_intents = []
    
    for example in test_data:
        text = example["text"]
        true_intent = example["intent"]
        language = example["language"]
        
        # Parse the command using our enhanced model
        try:
            parsed_result = parse_multilingual_command(text)
            pred_intent = parsed_result["intent"]
            confidence = parsed_result["confidence"]
            detected_language = parsed_result["language"]
            is_mixed = parsed_result["is_mixed_language"]
            
            # Store results
            results.append({
                "text": text,
                "true_intent": true_intent,
                "pred_intent": pred_intent,
                "true_language": language,
                "detected_language": detected_language,
                "is_mixed": is_mixed,
                "confidence": confidence,
                "correct": pred_intent == true_intent
            })
            
            true_intents.append(true_intent)
            pred_intents.append(pred_intent)
            
        except Exception as e:
            print(f"Error processing example: {text}")
            print(f"Error: {e}")
            
            # Add failed result
            results.append({
                "text": text,
                "true_intent": true_intent,
                "pred_intent": "error",
                "true_language": language,
                "detected_language": "unknown",
                "is_mixed": False,
                "confidence": 0.0,
                "correct": False,
                "error": str(e)
            })
            
            true_intents.append(true_intent)
            pred_intents.append("error")
    
    return results, true_intents, pred_intents

def calculate_metrics(results):
    """Calculate accuracy metrics by language and intent"""
    # Overall accuracy
    correct = sum(1 for r in results if r["correct"])
    total = len(results)
    overall_accuracy = correct / total if total > 0 else 0
    
    # Accuracy by language
    language_metrics = {}
    for lang in ["en", "hi", "mixed"]:
        lang_results = [r for r in results if r["true_language"] == lang]
        lang_correct = sum(1 for r in lang_results if r["correct"])
        lang_total = len(lang_results)
        lang_accuracy = lang_correct / lang_total if lang_total > 0 else 0
        
        language_metrics[lang] = {
            "accuracy": lang_accuracy,
            "correct": lang_correct,
            "total": lang_total
        }
    
    # Accuracy by intent
    intent_metrics = {}
    all_intents = set(r["true_intent"] for r in results)
    
    for intent in all_intents:
        intent_results = [r for r in results if r["true_intent"] == intent]
        intent_correct = sum(1 for r in intent_results if r["correct"])
        intent_total = len(intent_results)
        intent_accuracy = intent_correct / intent_total if intent_total > 0 else 0
        
        # Further break down by language
        lang_breakdown = {}
        for lang in ["en", "hi", "mixed"]:
            lang_intent_results = [r for r in intent_results if r["true_language"] == lang]
            lang_intent_correct = sum(1 for r in lang_intent_results if r["correct"])
            lang_intent_total = len(lang_intent_results)
            lang_intent_accuracy = lang_intent_correct / lang_intent_total if lang_intent_total > 0 else 0
            
            lang_breakdown[lang] = {
                "accuracy": lang_intent_accuracy,
                "correct": lang_intent_correct,
                "total": lang_intent_total
            }
        
        intent_metrics[intent] = {
            "accuracy": intent_accuracy,
            "correct": intent_correct,
            "total": intent_total,
            "by_language": lang_breakdown
        }
    
    # Language detection accuracy
    lang_detection_correct = sum(1 for r in results 
                               if (r["true_language"] == r["detected_language"]) or 
                                  (r["true_language"] == "mixed" and r["is_mixed"]))
    lang_detection_accuracy = lang_detection_correct / total if total > 0 else 0
    
    # Mixed language detection accuracy
    mixed_results = [r for r in results if r["true_language"] == "mixed"]
    mixed_correct = sum(1 for r in mixed_results if r["is_mixed"])
    mixed_total = len(mixed_results)
    mixed_detection_accuracy = mixed_correct / mixed_total if mixed_total > 0 else 0
    
    metrics = {
        "overall_accuracy": overall_accuracy,
        "by_language": language_metrics,
        "by_intent": intent_metrics,
        "language_detection_accuracy": lang_detection_accuracy,
        "mixed_language_detection_accuracy": mixed_detection_accuracy
    }
    
    return metrics

def generate_confusion_matrix(true_intents, pred_intents):
    """Generate confusion matrix for intent classification"""
    # Get unique intents (including 'error' for failed predictions)
    all_intents = sorted(list(set(true_intents + pred_intents)))
    
    # Create confusion matrix
    cm = confusion_matrix(true_intents, pred_intents, labels=all_intents)
    
    return cm, all_intents

def plot_confusion_matrix(cm, intent_labels, output_dir="./evaluation_results"):
    """Plot and save confusion matrix as image"""
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=intent_labels, yticklabels=intent_labels)
    plt.xlabel("Predicted Intent")
    plt.ylabel("True Intent")
    plt.title("Intent Classification Confusion Matrix")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close()

def plot_accuracy_by_language(metrics, output_dir="./evaluation_results"):
    """Plot and save accuracy by language"""
    languages = list(metrics["by_language"].keys())
    accuracies = [metrics["by_language"][lang]["accuracy"] for lang in languages]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(languages, accuracies, color=["blue", "green", "orange"])
    
    # Add accuracy values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f"{height:.2f}", ha="center", va="bottom")
    
    plt.xlabel("Language")
    plt.ylabel("Accuracy")
    plt.title("Intent Recognition Accuracy by Language")
    plt.ylim(0, 1.1)  # Set y-axis limit to 0-1.1 for better visualization
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "accuracy_by_language.png"))
    plt.close()

def plot_accuracy_by_intent(metrics, output_dir="./evaluation_results"):
    """Plot and save accuracy by intent"""
    intents = list(metrics["by_intent"].keys())
    accuracies = [metrics["by_intent"][intent]["accuracy"] for intent in intents]
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(intents, accuracies)
    
    # Add accuracy values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f"{height:.2f}", ha="center", va="bottom")
    
    plt.xlabel("Intent")
    plt.ylabel("Accuracy")
    plt.title("Intent Recognition Accuracy by Intent")
    plt.ylim(0, 1.1)  # Set y-axis limit to 0-1.1 for better visualization
    plt.xticks(rotation=45, ha="right")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "accuracy_by_intent.png"))
    plt.close()

def save_evaluation_results(results, metrics, cm, intent_labels, output_dir="./evaluation_results"):
    """Save evaluation results to JSON file"""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save detailed results
    with open(os.path.join(output_dir, "evaluation_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Save metrics
    with open(os.path.join(output_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    # Save confusion matrix
    cm_dict = {
        "matrix": cm.tolist(),
        "intent_labels": intent_labels
    }
    with open(os.path.join(output_dir, "confusion_matrix.json"), "w", encoding="utf-8") as f:
        json.dump(cm_dict, f, ensure_ascii=False, indent=2)
    
    # Generate summary report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = f"# Multilingual NLP Model Evaluation Report\n\n"
    summary += f"Generated on: {timestamp}\n\n"
    
    summary += f"## Overall Performance\n\n"
    summary += f"- Overall Accuracy: {metrics['overall_accuracy']:.4f}\n"
    summary += f"- Language Detection Accuracy: {metrics['language_detection_accuracy']:.4f}\n"
    summary += f"- Mixed Language Detection Accuracy: {metrics['mixed_language_detection_accuracy']:.4f}\n\n"
    
    summary += f"## Performance by Language\n\n"
    summary += f"| Language | Accuracy | Correct | Total |\n"
    summary += f"| -------- | -------- | ------- | ----- |\n"
    for lang, lang_metrics in metrics["by_language"].items():
        summary += f"| {lang} | {lang_metrics['accuracy']:.4f} | {lang_metrics['correct']} | {lang_metrics['total']} |\n"
    summary += "\n"
    
    summary += f"## Performance by Intent\n\n"
    summary += f"| Intent | Accuracy | Correct | Total |\n"
    summary += f"| ------ | -------- | ------- | ----- |\n"
    for intent, intent_metrics in metrics["by_intent"].items():
        summary += f"| {intent} | {intent_metrics['accuracy']:.4f} | {intent_metrics['correct']} | {intent_metrics['total']} |\n"
    summary += "\n"
    
    summary += f"## Common Errors\n\n"
    errors = [r for r in results if not r["correct"]]
    if errors:
        summary += f"Top 10 errors (out of {len(errors)} total errors):\n\n"
        summary += f"| Text | True Intent | Predicted Intent | Language |\n"
        summary += f"| ---- | ----------- | --------------- | -------- |\n"
        for error in errors[:10]:
            summary += f"| {error['text']} | {error['true_intent']} | {error['pred_intent']} | {error['true_language']} |\n"
    else:
        summary += "No errors found.\n"
    
    # Save summary report
    with open(os.path.join(output_dir, "evaluation_summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"Evaluation results saved to {output_dir}")

def main():
    # Load test data
    print("Loading test data...")
    test_data = load_test_data()
    
    if not test_data:
        print("No test data available. Please generate test data first.")
        return
    
    print(f"Loaded {len(test_data)} test examples")
    
    # Evaluate model
    print("Evaluating model...")
    results, true_intents, pred_intents = evaluate_model(test_data)
    
    # Calculate metrics
    print("Calculating metrics...")
    metrics = calculate_metrics(results)
    
    # Generate confusion matrix
    print("Generating confusion matrix...")
    cm, intent_labels = generate_confusion_matrix(true_intents, pred_intents)
    
    # Plot results
    print("Plotting results...")
    plot_confusion_matrix(cm, intent_labels)
    plot_accuracy_by_language(metrics)
    plot_accuracy_by_intent(metrics)
    
    # Save results
    print("Saving evaluation results...")
    save_evaluation_results(results, metrics, cm, intent_labels)
    
    # Print summary
    print("\nEvaluation Summary:")
    print(f"Overall Accuracy: {metrics['overall_accuracy']:.4f}")
    print(f"Language Detection Accuracy: {metrics['language_detection_accuracy']:.4f}")
    print(f"Mixed Language Detection Accuracy: {metrics['mixed_language_detection_accuracy']:.4f}")
    
    print("\nAccuracy by Language:")
    for lang, lang_metrics in metrics["by_language"].items():
        print(f"{lang}: {lang_metrics['accuracy']:.4f} ({lang_metrics['correct']}/{lang_metrics['total']})")
    
    print("\nAccuracy by Intent:")
    for intent, intent_metrics in sorted(metrics["by_intent"].items()):
        print(f"{intent}: {intent_metrics['accuracy']:.4f} ({intent_metrics['correct']}/{intent_metrics['total']})")

if __name__ == "__main__":
    main()