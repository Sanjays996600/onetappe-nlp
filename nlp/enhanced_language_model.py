#!/usr/bin/env python3
"""
Enhanced Language Model for Multilingual NLP Support

This module provides advanced language detection, intent recognition, and entity extraction
for both English and Hindi languages, with support for mixed language inputs.

It integrates transformer-based models for improved accuracy and robustness.
"""

import re
import json
import spacy
import torch
import numpy as np
from langdetect import detect, DetectorFactory
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from datetime import datetime, timedelta

# Set seed for reproducibility in langdetect
DetectorFactory.seed = 0

# Define character ranges for language detection
HINDI_CHAR_RANGE = r'[\u0900-\u097F]'
ENGLISH_CHAR_RANGE = r'[a-zA-Z]'

# Load spaCy models
try:
    # Try to load English model
    nlp_en = spacy.load("en_core_web_md")
except OSError:
    print("English model not found. Please download it using: python -m spacy download en_core_web_md")
    nlp_en = None

try:
    # Try to load multilingual model for Hindi support
    nlp_xx = spacy.load("xx_ent_wiki_sm")
except OSError:
    print("Multilingual model not found. Please download it using: python -m spacy download xx_ent_wiki_sm")
    nlp_xx = None

# Initialize transformer models for intent classification
class TransformerIntentClassifier:
    def __init__(self):
        self.model_initialized = False
        self.tokenizer = None
        self.model = None
        self.intent_labels = [
            "get_inventory", "get_low_stock", "get_report", "get_top_products",
            "get_customer_data", "add_product", "edit_stock", "get_orders", "search_product"
        ]
    
    def initialize(self):
        """Initialize the transformer model (lazy loading to save resources)"""
        try:
            # Using a smaller model for efficiency
            model_name = "distilbert-base-uncased"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(self.intent_labels))
            self.model_initialized = True
            print("Transformer model initialized successfully")
        except Exception as e:
            print(f"Error initializing transformer model: {e}")
            self.model_initialized = False
    
    def predict_intent(self, text):
        """Predict intent using transformer model"""
        if not self.model_initialized:
            self.initialize()
        
        if not self.model_initialized:
            return None, 0.0  # Return None if initialization failed
        
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)
            
            intent = self.intent_labels[predicted_class.item()]
            confidence_score = confidence.item()
            
            return intent, confidence_score
        except Exception as e:
            print(f"Error predicting intent with transformer: {e}")
            return None, 0.0

# Initialize the transformer intent classifier
transformer_classifier = TransformerIntentClassifier()

# Enhanced language detection
def detect_language_with_confidence(text):
    """Detect language with confidence score using character frequency analysis"""
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    
    total_chars = hindi_chars + english_chars
    if total_chars == 0:
        # If no Hindi or English characters found, use langdetect as fallback
        try:
            lang = detect(text)
            return "hi" if lang == "hi" else "en", 0.6  # Lower confidence for fallback
        except:
            return "en", 0.5  # Default to English with low confidence
    
    hindi_ratio = hindi_chars / total_chars
    english_ratio = english_chars / total_chars
    
    # Use a threshold to determine language
    # If more than 30% of characters are Hindi, classify as Hindi
    if hindi_ratio > 0.3:
        return "hi", hindi_ratio
    else:
        return "en", english_ratio

def detect_mixed_language(text):
    """Detect if text contains mixed languages and provide detailed analysis"""
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    
    total_chars = hindi_chars + english_chars
    if total_chars == 0:
        return False, {"primary": "en", "hindi_ratio": 0, "english_ratio": 0}
    
    hindi_ratio = hindi_chars / total_chars
    english_ratio = english_chars / total_chars
    
    # Determine primary language
    primary = "hi" if hindi_ratio > english_ratio else "en"
    
    # If both languages have significant presence (>20%), consider it mixed
    is_mixed = hindi_ratio > 0.2 and english_ratio > 0.2
    
    if is_mixed:
        # Extract segments of each language
        hindi_segments = re.findall(f"{HINDI_CHAR_RANGE}+", text)
        english_segments = re.findall(f"{ENGLISH_CHAR_RANGE}+", text)
        
        return True, {
            "primary": primary,
            "hindi_ratio": hindi_ratio,
            "english_ratio": english_ratio,
            "segments": {
                "hi": hindi_segments,
                "en": english_segments
            }
        }
    
    return False, {
        "primary": primary,
        "hindi_ratio": hindi_ratio,
        "english_ratio": english_ratio
    }

def handle_mixed_language_input(text):
    """Process mixed language input and suggest handling strategy"""
    is_mixed, lang_info = detect_mixed_language(text)
    
    if not is_mixed:
        return {
            "is_mixed": False,
            "primary_language": lang_info["primary"],
            "strategy": "use_primary"
        }
    
    # For mixed language, determine if we should split or use primary
    if lang_info["hindi_ratio"] > 0.6:
        strategy = "use_hindi"
    elif lang_info["english_ratio"] > 0.6:
        strategy = "use_english"
    else:
        strategy = "process_segments"
    
    return {
        "is_mixed": True,
        "primary_language": lang_info["primary"],
        "hindi_ratio": lang_info["hindi_ratio"],
        "english_ratio": lang_info["english_ratio"],
        "segments": lang_info.get("segments", {}),
        "strategy": strategy
    }

# Enhanced intent recognition using hybrid approach (rules + ML)
def recognize_intent(text, language="en", use_ml=True):
    """Recognize intent using a hybrid approach of rules and ML"""
    # First try ML-based intent recognition if enabled
    if use_ml and transformer_classifier.model_initialized:
        intent, confidence = transformer_classifier.predict_intent(text)
        if intent and confidence > 0.7:  # Only use ML result if confidence is high
            return intent, confidence
    
    # Fall back to rule-based approach
    from intent_handler import INTENT_PATTERNS
    from hindi_support import HINDI_INTENT_PATTERNS
    
    patterns = INTENT_PATTERNS if language == "en" else HINDI_INTENT_PATTERNS
    
    for intent, intent_patterns in patterns.items():
        for pattern in intent_patterns:
            match = re.search(pattern, text, re.IGNORECASE if language == "en" else 0)
            if match:
                return intent, 0.9  # High confidence for rule-based matches
    
    # If no intent is recognized, try the other language's patterns as fallback
    fallback_patterns = HINDI_INTENT_PATTERNS if language == "en" else INTENT_PATTERNS
    
    for intent, intent_patterns in fallback_patterns.items():
        for pattern in intent_patterns:
            match = re.search(pattern, text, re.IGNORECASE if language != "en" else 0)
            if match:
                return intent, 0.7  # Lower confidence for fallback language
    
    return "unknown", 0.0

# Enhanced entity extraction using spaCy and rules
def extract_entities(text, intent, language="en"):
    """Extract entities using a hybrid approach of spaCy and rules"""
    entities = {}
    
    # Use appropriate spaCy model based on language
    nlp = nlp_en if language == "en" and nlp_en else nlp_xx
    
    if intent == "edit_stock":
        if language == "en":
            from intent_handler import extract_edit_stock_details
            entities = extract_edit_stock_details(text)
        else:  # Hindi
            from hindi_support import extract_hindi_edit_stock_details
            entities = extract_hindi_edit_stock_details(text)
            
        # Enhance with spaCy if available
        if nlp and not entities.get("product_name"):
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PRODUCT", "ORG", "MISC"]:
                    entities["product_name"] = ent.text
                    break
    
    elif intent == "add_product":
        if language == "en":
            from intent_handler import extract_product_details
            entities = extract_product_details(text)
        else:  # Hindi
            from hindi_support import extract_hindi_product_details
            entities = extract_hindi_product_details(text)
    
    elif intent in ["get_orders", "get_report"]:
        # Extract time range for reports and orders
        if language == "en":
            from intent_handler import extract_report_range, extract_order_range_details
            if intent == "get_report":
                entities = extract_report_range(text)
            else:  # get_orders
                entities = extract_order_range_details(text)
        else:  # Hindi
            from hindi_support import extract_hindi_report_range, extract_hindi_order_range_details
            if intent == "get_report":
                entities = extract_hindi_report_range(text)
            else:  # get_orders
                entities = extract_hindi_order_range_details(text)
    
    elif intent == "search_product":
        if language == "en":
            from intent_handler import extract_search_product_details
            entities = extract_search_product_details(text)
        else:  # Hindi
            from hindi_support import extract_hindi_search_product_details
            entities = extract_hindi_search_product_details(text)
    
    elif intent == "get_low_stock":
        if language == "en":
            from intent_handler import extract_get_low_stock_details
            entities = extract_get_low_stock_details(text)
        else:  # Hindi
            from hindi_support import extract_hindi_get_low_stock_details
            entities = extract_hindi_get_low_stock_details(text)
    
    return entities

# Enhanced multilingual command parser
def parse_multilingual_command(text):
    """Parse command with enhanced language detection and mixed language support"""
    # Detect if text contains mixed languages
    is_mixed, lang_info = detect_mixed_language(text)
    primary_language = lang_info["primary"]
    
    # Normalize text (lowercase for English, keep as is for Hindi)
    normalized_text = text.lower() if primary_language == "en" else text
    
    # Recognize intent
    intent, confidence = recognize_intent(text, primary_language)
    
    # Extract entities
    entities = extract_entities(text, intent, primary_language)
    
    # Format response
    response = {
        "original_text": text,
        "raw_text": text,  # Adding raw_text for compatibility
        "normalized_text": normalized_text,
        "language": primary_language,
        "is_mixed_language": is_mixed,
        "intent": intent,
        "confidence": confidence,
        "entities": entities,
        "status": "success" if intent != "unknown" else "failed"
    }
    
    # Add language analysis for mixed language inputs
    if is_mixed:
        response["language_analysis"] = lang_info
    
    return response

# Training function for the transformer model
def train_intent_classifier(training_data):
    """Train the transformer model with custom data"""
    if not transformer_classifier.model_initialized:
        transformer_classifier.initialize()
    
    if not transformer_classifier.model_initialized:
        print("Failed to initialize transformer model for training")
        return False
    
    try:
        # Prepare training data
        texts = [item["text"] for item in training_data]
        labels = [transformer_classifier.intent_labels.index(item["intent"]) for item in training_data]
        
        # Tokenize inputs
        tokenized_inputs = transformer_classifier.tokenizer(
            texts, 
            padding=True, 
            truncation=True, 
            return_tensors="pt"
        )
        
        # Create dataset
        dataset = torch.utils.data.TensorDataset(
            tokenized_inputs["input_ids"],
            tokenized_inputs["attention_mask"],
            torch.tensor(labels)
        )
        
        # Create data loader
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True)
        
        # Set up optimizer
        optimizer = torch.optim.AdamW(transformer_classifier.model.parameters(), lr=5e-5)
        
        # Training loop
        transformer_classifier.model.train()
        for epoch in range(3):  # 3 epochs
            total_loss = 0
            for batch in dataloader:
                input_ids, attention_mask, labels = batch
                
                # Forward pass
                outputs = transformer_classifier.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_loss += loss.item()
                
                # Backward pass and optimization
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            
            print(f"Epoch {epoch+1}, Loss: {total_loss/len(dataloader)}")
        
        # Save the model
        transformer_classifier.model.save_pretrained("./intent_classifier_model")
        transformer_classifier.tokenizer.save_pretrained("./intent_classifier_tokenizer")
        
        return True
    
    except Exception as e:
        print(f"Error training transformer model: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Test language detection
    test_texts = [
        "Show me my inventory",
        "मेरा इन्वेंटरी दिखाओ",
        "Update rice stock to 50",
        "चावल का स्टॉक 50 करो",
        "Show me चावल inventory",  # Mixed
    ]
    
    print("\nTesting language detection:")
    for text in test_texts:
        lang, conf = detect_language_with_confidence(text)
        is_mixed, info = detect_mixed_language(text)
        print(f"Text: {text}")
        print(f"Language: {lang}, Confidence: {conf:.2f}")
        print(f"Mixed: {is_mixed}")
        if is_mixed:
            print(f"Primary: {info['primary']}")
            print(f"Hindi segments: {info['segments'].get('hi', [])}")
            print(f"English segments: {info['segments'].get('en', [])}")
        print()
    
    # Test intent recognition
    print("\nTesting intent recognition:")
    for text in test_texts:
        result = parse_multilingual_command(text)
        print(f"Text: {text}")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result.get('confidence', 0):.2f}")
        print(f"Entities: {result['entities']}")
        print(f"Language: {result['language']}")
        print(f"Mixed: {result['is_mixed_language']}")
        print()