import os
import json
import random
import numpy as np
import pandas as pd
import spacy
import pickle
from typing import Dict, List, Tuple, Any, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

# Try to import the multilingual processor
try:
    from multilingual_processor import MultilingualProcessor
except ImportError:
    try:
        from OneTappeProject.nlp.multilingual_processor import MultilingualProcessor
    except ImportError:
        print("Could not import MultilingualProcessor. Make sure the module is available.")


class ModelTrainer:
    """A class for training and evaluating NLP models for multilingual intent recognition."""
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the model trainer.
        
        Args:
            data_path: Path to the training data file. If None, default training data will be used.
        """
        self.data_path = data_path
        self.training_data = None
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
        self.label_encoder = LabelEncoder()
        self.model = None
        self.processor = MultilingualProcessor()
        
        # Load or create training data
        if data_path and os.path.exists(data_path):
            self.load_training_data(data_path)
        else:
            self.create_default_training_data()
    
    def load_training_data(self, data_path: str) -> None:
        """Load training data from a file.
        
        Args:
            data_path: Path to the training data file.
        """
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            print(f"Loaded {len(self.training_data)} training examples from {data_path}")
        except Exception as e:
            print(f"Error loading training data: {e}")
            self.create_default_training_data()
    
    def create_default_training_data(self) -> None:
        """Create default training data for intent recognition."""
        self.training_data = [
            # English examples
            {"text": "Show inventory", "intent": "get_inventory", "language": "en"},
            {"text": "Get inventory", "intent": "get_inventory", "language": "en"},
            {"text": "Display inventory", "intent": "get_inventory", "language": "en"},
            {"text": "View inventory", "intent": "get_inventory", "language": "en"},
            {"text": "What inventory do we have", "intent": "get_inventory", "language": "en"},
            {"text": "How much stock is available", "intent": "get_inventory", "language": "en"},
            {"text": "Current inventory", "intent": "get_inventory", "language": "en"},
            
            {"text": "Show low stock", "intent": "get_low_stock", "language": "en"},
            {"text": "Display low inventory", "intent": "get_low_stock", "language": "en"},
            {"text": "View limited stock", "intent": "get_low_stock", "language": "en"},
            {"text": "What products are low in stock", "intent": "get_low_stock", "language": "en"},
            {"text": "Which items are limited in inventory", "intent": "get_low_stock", "language": "en"},
            {"text": "Low stock report", "intent": "get_low_stock", "language": "en"},
            {"text": "Low stock alert", "intent": "get_low_stock", "language": "en"},
            
            {"text": "Update stock", "intent": "edit_stock", "language": "en"},
            {"text": "Change inventory", "intent": "edit_stock", "language": "en"},
            {"text": "Modify stock", "intent": "edit_stock", "language": "en"},
            {"text": "Edit inventory", "intent": "edit_stock", "language": "en"},
            {"text": "Set stock", "intent": "edit_stock", "language": "en"},
            {"text": "Add 10 items", "intent": "edit_stock", "language": "en"},
            {"text": "Remove 5 products", "intent": "edit_stock", "language": "en"},
            {"text": "Increase stock by 20 units", "intent": "edit_stock", "language": "en"},
            {"text": "Decrease inventory by 15", "intent": "edit_stock", "language": "en"},
            {"text": "Add inventory", "intent": "edit_stock", "language": "en"},
            {"text": "Remove stock", "intent": "edit_stock", "language": "en"},
            
            {"text": "Search product", "intent": "search_product", "language": "en"},
            {"text": "Find item", "intent": "search_product", "language": "en"},
            {"text": "Look for product", "intent": "search_product", "language": "en"},
            {"text": "Show product", "intent": "search_product", "language": "en"},
            {"text": "Get item", "intent": "search_product", "language": "en"},
            {"text": "Display product", "intent": "search_product", "language": "en"},
            {"text": "View item", "intent": "search_product", "language": "en"},
            {"text": "Details of product", "intent": "search_product", "language": "en"},
            {"text": "Info about item", "intent": "search_product", "language": "en"},
            {"text": "Information for product", "intent": "search_product", "language": "en"},
            
            {"text": "Show orders", "intent": "get_orders", "language": "en"},
            {"text": "Get sales", "intent": "get_orders", "language": "en"},
            {"text": "Display orders", "intent": "get_orders", "language": "en"},
            {"text": "View sales", "intent": "get_orders", "language": "en"},
            {"text": "Recent orders", "intent": "get_orders", "language": "en"},
            {"text": "Today's sales", "intent": "get_orders", "language": "en"},
            {"text": "Yesterday's orders", "intent": "get_orders", "language": "en"},
            {"text": "This week's sales", "intent": "get_orders", "language": "en"},
            {"text": "This month's orders", "intent": "get_orders", "language": "en"},
            {"text": "Last 7 days orders", "intent": "get_orders", "language": "en"},
            {"text": "Orders report", "intent": "get_orders", "language": "en"},
            {"text": "Sales summary", "intent": "get_orders", "language": "en"},
            {"text": "Orders data", "intent": "get_orders", "language": "en"},
            
            {"text": "Show report", "intent": "get_report", "language": "en"},
            {"text": "Get report", "intent": "get_report", "language": "en"},
            {"text": "Display report", "intent": "get_report", "language": "en"},
            {"text": "View report", "intent": "get_report", "language": "en"},
            {"text": "Generate report", "intent": "get_report", "language": "en"},
            {"text": "Sales report", "intent": "get_report", "language": "en"},
            {"text": "Revenue report", "intent": "get_report", "language": "en"},
            {"text": "Profit report", "intent": "get_report", "language": "en"},
            {"text": "Performance report", "intent": "get_report", "language": "en"},
            {"text": "Recent report", "intent": "get_report", "language": "en"},
            {"text": "Today's report", "intent": "get_report", "language": "en"},
            {"text": "Yesterday's report", "intent": "get_report", "language": "en"},
            {"text": "This week's report", "intent": "get_report", "language": "en"},
            {"text": "This month's report", "intent": "get_report", "language": "en"},
            {"text": "Last 7 days report", "intent": "get_report", "language": "en"},
            
            # Hindi examples
            {"text": "इन्वेंटरी दिखाओ", "intent": "get_inventory", "language": "hi"},
            {"text": "स्टॉक दिखाओ", "intent": "get_inventory", "language": "hi"},
            {"text": "इन्वेंटरी बताओ", "intent": "get_inventory", "language": "hi"},
            {"text": "स्टॉक बताओ", "intent": "get_inventory", "language": "hi"},
            {"text": "कितना इन्वेंटरी है", "intent": "get_inventory", "language": "hi"},
            {"text": "क्या स्टॉक उपलब्ध है", "intent": "get_inventory", "language": "hi"},
            {"text": "वर्तमान इन्वेंटरी", "intent": "get_inventory", "language": "hi"},
            {"text": "वर्तमान स्टॉक", "intent": "get_inventory", "language": "hi"},
            
            {"text": "कम इन्वेंटरी दिखाओ", "intent": "get_low_stock", "language": "hi"},
            {"text": "सीमित स्टॉक दिखाओ", "intent": "get_low_stock", "language": "hi"},
            {"text": "कम इन्वेंटरी बताओ", "intent": "get_low_stock", "language": "hi"},
            {"text": "सीमित स्टॉक बताओ", "intent": "get_low_stock", "language": "hi"},
            {"text": "कौन प्रोडक्ट्स कम स्टॉक में हैं", "intent": "get_low_stock", "language": "hi"},
            {"text": "क्या आइटम्स सीमित इन्वेंटरी में हैं", "intent": "get_low_stock", "language": "hi"},
            {"text": "कम स्टॉक रिपोर्ट", "intent": "get_low_stock", "language": "hi"},
            {"text": "लो स्टॉक अलर्ट", "intent": "get_low_stock", "language": "hi"},
            
            {"text": "इन्वेंटरी अपडेट करो", "intent": "edit_stock", "language": "hi"},
            {"text": "स्टॉक बदलो", "intent": "edit_stock", "language": "hi"},
            {"text": "इन्वेंटरी संशोधित करो", "intent": "edit_stock", "language": "hi"},
            {"text": "स्टॉक एडिट करो", "intent": "edit_stock", "language": "hi"},
            {"text": "स्टॉक सेट करो", "intent": "edit_stock", "language": "hi"},
            {"text": "10 आइटम्स जोड़ो", "intent": "edit_stock", "language": "hi"},
            {"text": "5 प्रोडक्ट्स हटाओ", "intent": "edit_stock", "language": "hi"},
            {"text": "20 यूनिट्स स्टॉक बढ़ाओ", "intent": "edit_stock", "language": "hi"},
            {"text": "15 इन्वेंटरी घटाओ", "intent": "edit_stock", "language": "hi"},
            {"text": "इन्वेंटरी जोड़ो", "intent": "edit_stock", "language": "hi"},
            {"text": "स्टॉक हटाओ", "intent": "edit_stock", "language": "hi"},
            
            {"text": "प्रोडक्ट खोजो", "intent": "search_product", "language": "hi"},
            {"text": "आइटम ढूंढो", "intent": "search_product", "language": "hi"},
            {"text": "प्रोडक्ट सर्च करो", "intent": "search_product", "language": "hi"},
            {"text": "प्रोडक्ट दिखाओ", "intent": "search_product", "language": "hi"},
            {"text": "आइटम बताओ", "intent": "search_product", "language": "hi"},
            {"text": "प्रोडक्ट के विवरण", "intent": "search_product", "language": "hi"},
            {"text": "आइटम की जानकारी", "intent": "search_product", "language": "hi"},
            {"text": "प्रोडक्ट के डिटेल्स", "intent": "search_product", "language": "hi"},
            
            {"text": "ऑर्डर्स दिखाओ", "intent": "get_orders", "language": "hi"},
            {"text": "सेल्स दिखाओ", "intent": "get_orders", "language": "hi"},
            {"text": "बिक्री दिखाओ", "intent": "get_orders", "language": "hi"},
            {"text": "ऑर्डर्स बताओ", "intent": "get_orders", "language": "hi"},
            {"text": "सेल्स बताओ", "intent": "get_orders", "language": "hi"},
            {"text": "हाल के ऑर्डर्स", "intent": "get_orders", "language": "hi"},
            {"text": "आज के सेल्स", "intent": "get_orders", "language": "hi"},
            {"text": "कल के ऑर्डर्स", "intent": "get_orders", "language": "hi"},
            {"text": "इस हफ्ते के सेल्स", "intent": "get_orders", "language": "hi"},
            {"text": "इस महीने के ऑर्डर्स", "intent": "get_orders", "language": "hi"},
            {"text": "पिछले 7 दिनों के सेल्स", "intent": "get_orders", "language": "hi"},
            {"text": "ऑर्डर्स रिपोर्ट", "intent": "get_orders", "language": "hi"},
            {"text": "सेल्स सारांश", "intent": "get_orders", "language": "hi"},
            {"text": "ऑर्डर्स डेटा", "intent": "get_orders", "language": "hi"},
            
            {"text": "रिपोर्ट दिखाओ", "intent": "get_report", "language": "hi"},
            {"text": "रिपोर्ट बताओ", "intent": "get_report", "language": "hi"},
            {"text": "रिपोर्ट जनरेट करो", "intent": "get_report", "language": "hi"},
            {"text": "सेल्स रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "रेवेन्यू रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "प्रॉफिट रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "परफॉरमेंस रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "हाल के रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "आज के रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "कल के रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "इस हफ्ते के रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "इस महीने के रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "पिछले 7 दिनों के रिपोर्ट", "intent": "get_report", "language": "hi"},
            
            # Transliterated Hindi examples
            {"text": "Inventory dikhao", "intent": "get_inventory", "language": "mixed"},
            {"text": "Stock batao", "intent": "get_inventory", "language": "mixed"},
            {"text": "Kitna inventory hai", "intent": "get_inventory", "language": "mixed"},
            {"text": "Kya stock available hai", "intent": "get_inventory", "language": "mixed"},
            {"text": "Vartaman inventory", "intent": "get_inventory", "language": "mixed"},
            
            {"text": "Kam inventory dikhao", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Limited stock batao", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Kaun products kam stock mein hain", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Kya items limited inventory mein hain", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Kam stock report", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Low stock alert", "intent": "get_low_stock", "language": "mixed"},
            
            {"text": "Inventory update karo", "intent": "edit_stock", "language": "mixed"},
            {"text": "Stock badlo", "intent": "edit_stock", "language": "mixed"},
            {"text": "Inventory edit karo", "intent": "edit_stock", "language": "mixed"},
            {"text": "Stock set karo", "intent": "edit_stock", "language": "mixed"},
            {"text": "10 items jodo", "intent": "edit_stock", "language": "mixed"},
            {"text": "5 products hatao", "intent": "edit_stock", "language": "mixed"},
            {"text": "20 units stock badhao", "intent": "edit_stock", "language": "mixed"},
            {"text": "15 inventory ghatao", "intent": "edit_stock", "language": "mixed"},
            {"text": "Inventory jodo", "intent": "edit_stock", "language": "mixed"},
            {"text": "Stock hatao", "intent": "edit_stock", "language": "mixed"},
            
            {"text": "Product khojo", "intent": "search_product", "language": "mixed"},
            {"text": "Item dhundho", "intent": "search_product", "language": "mixed"},
            {"text": "Product search karo", "intent": "search_product", "language": "mixed"},
            {"text": "Product dikhao", "intent": "search_product", "language": "mixed"},
            {"text": "Item batao", "intent": "search_product", "language": "mixed"},
            {"text": "Product ke details", "intent": "search_product", "language": "mixed"},
            {"text": "Item ki jankari", "intent": "search_product", "language": "mixed"},
            
            {"text": "Orders dikhao", "intent": "get_orders", "language": "mixed"},
            {"text": "Sales batao", "intent": "get_orders", "language": "mixed"},
            {"text": "Bikri dikhao", "intent": "get_orders", "language": "mixed"},
            {"text": "Hal ke orders", "intent": "get_orders", "language": "mixed"},
            {"text": "Aaj ke sales", "intent": "get_orders", "language": "mixed"},
            {"text": "Kal ke orders", "intent": "get_orders", "language": "mixed"},
            {"text": "Is hafte ke sales", "intent": "get_orders", "language": "mixed"},
            {"text": "Is mahine ke orders", "intent": "get_orders", "language": "mixed"},
            {"text": "Pichhle 7 dino ke sales", "intent": "get_orders", "language": "mixed"},
            {"text": "Orders report", "intent": "get_orders", "language": "mixed"},
            {"text": "Sales summary", "intent": "get_orders", "language": "mixed"},
            
            {"text": "Report dikhao", "intent": "get_report", "language": "mixed"},
            {"text": "Report batao", "intent": "get_report", "language": "mixed"},
            {"text": "Report generate karo", "intent": "get_report", "language": "mixed"},
            {"text": "Sales report", "intent": "get_report", "language": "mixed"},
            {"text": "Revenue report", "intent": "get_report", "language": "mixed"},
            {"text": "Profit report", "intent": "get_report", "language": "mixed"},
            {"text": "Performance report", "intent": "get_report", "language": "mixed"},
            {"text": "Hal ke report", "intent": "get_report", "language": "mixed"},
            {"text": "Aaj ke report", "intent": "get_report", "language": "mixed"},
            {"text": "Kal ke report", "intent": "get_report", "language": "mixed"},
            {"text": "Is hafte ke report", "intent": "get_report", "language": "mixed"},
            {"text": "Is mahine ke report", "intent": "get_report", "language": "mixed"},
            {"text": "Pichhle 7 dino ke report", "intent": "get_report", "language": "mixed"},
            
            # Mixed language examples
            {"text": "Show इन्वेंटरी", "intent": "get_inventory", "language": "mixed"},
            {"text": "Get स्टॉक", "intent": "get_inventory", "language": "mixed"},
            {"text": "Display इन्वेंटरी", "intent": "get_inventory", "language": "mixed"},
            {"text": "View स्टॉक", "intent": "get_inventory", "language": "mixed"},
            {"text": "कितना inventory है", "intent": "get_inventory", "language": "mixed"},
            {"text": "क्या stock available है", "intent": "get_inventory", "language": "mixed"},
            {"text": "Current इन्वेंटरी", "intent": "get_inventory", "language": "mixed"},
            
            {"text": "Show कम स्टॉक", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Display सीमित इन्वेंटरी", "intent": "get_low_stock", "language": "mixed"},
            {"text": "View कम स्टॉक", "intent": "get_low_stock", "language": "mixed"},
            {"text": "कौन products कम stock में हैं", "intent": "get_low_stock", "language": "mixed"},
            {"text": "क्या items सीमित inventory में हैं", "intent": "get_low_stock", "language": "mixed"},
            {"text": "Low स्टॉक report", "intent": "get_low_stock", "language": "mixed"},
            {"text": "कम stock alert", "intent": "get_low_stock", "language": "mixed"},
            
            {"text": "Update स्टॉक", "intent": "edit_stock", "language": "mixed"},
            {"text": "Change इन्वेंटरी", "intent": "edit_stock", "language": "mixed"},
            {"text": "Modify स्टॉक", "intent": "edit_stock", "language": "mixed"},
            {"text": "Edit इन्वेंटरी", "intent": "edit_stock", "language": "mixed"},
            {"text": "Set स्टॉक", "intent": "edit_stock", "language": "mixed"},
            {"text": "Add 10 आइटम्स", "intent": "edit_stock", "language": "mixed"},
            {"text": "Remove 5 प्रोडक्ट्स", "intent": "edit_stock", "language": "mixed"},
            {"text": "Increase स्टॉक by 20 यूनिट्स", "intent": "edit_stock", "language": "mixed"},
            {"text": "Decrease इन्वेंटरी by 15", "intent": "edit_stock", "language": "mixed"},
            {"text": "Add इन्वेंटरी", "intent": "edit_stock", "language": "mixed"},
            {"text": "Remove स्टॉक", "intent": "edit_stock", "language": "mixed"},
            
            {"text": "Search प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            {"text": "Find आइटम", "intent": "search_product", "language": "mixed"},
            {"text": "Look for प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            {"text": "Show प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            {"text": "Get आइटम", "intent": "search_product", "language": "mixed"},
            {"text": "Display प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            {"text": "View आइटम", "intent": "search_product", "language": "mixed"},
            {"text": "Details of प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            {"text": "Info about आइटम", "intent": "search_product", "language": "mixed"},
            {"text": "Information for प्रोडक्ट", "intent": "search_product", "language": "mixed"},
            
            {"text": "Show ऑर्डर्स", "intent": "get_orders", "language": "mixed"},
            {"text": "Get सेल्स", "intent": "get_orders", "language": "mixed"},
            {"text": "Display ऑर्डर्स", "intent": "get_orders", "language": "mixed"},
            {"text": "View बिक्री", "intent": "get_orders", "language": "mixed"},
            {"text": "Recent ऑर्डर्स", "intent": "get_orders", "language": "mixed"},
            {"text": "Today's सेल्स", "intent": "get_orders", "language": "mixed"},
            {"text": "Yesterday's ऑर्डर्स", "intent": "get_orders", "language": "mixed"},
            {"text": "This week's सेल्स", "intent": "get_orders", "language": "mixed"},
            {"text": "This month's ऑर्डर्स", "intent": "get_orders", "language": "mixed"},
            {"text": "Last 7 days के सेल्स", "intent": "get_orders", "language": "mixed"},
            {"text": "ऑर्डर्स report", "intent": "get_orders", "language": "mixed"},
            {"text": "सेल्स summary", "intent": "get_orders", "language": "mixed"},
            {"text": "ऑर्डर्स data", "intent": "get_orders", "language": "mixed"},
            
            {"text": "Show रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Get रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Display रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "View रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Generate रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Sales रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Revenue रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Profit रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Performance रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Recent रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Today's रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Yesterday's रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "This week's रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "This month's रिपोर्ट", "intent": "get_report", "language": "mixed"},
            {"text": "Last 7 days के रिपोर्ट", "intent": "get_report", "language": "mixed"},
            
            # Report-specific examples with date ranges
            {"text": "Show report from January 1 to January 31", "intent": "get_report", "language": "en"},
            {"text": "Get report between February 15 and March 15", "intent": "get_report", "language": "en"},
            {"text": "Display report for April 1 to April 30", "intent": "get_report", "language": "en"},
            {"text": "View report from May 10 to May 20", "intent": "get_report", "language": "en"},
            
            {"text": "1 जनवरी से 31 जनवरी तक का रिपोर्ट दिखाओ", "intent": "get_report", "language": "hi"},
            {"text": "15 फरवरी से 15 मार्च के बीच का रिपोर्ट बताओ", "intent": "get_report", "language": "hi"},
            {"text": "1 अप्रैल से 30 अप्रैल तक का रिपोर्ट", "intent": "get_report", "language": "hi"},
            {"text": "10 मई से 20 मई तक का रिपोर्ट दिखाओ", "intent": "get_report", "language": "hi"},
            
            {"text": "1 January से 31 January तक का report दिखाओ", "intent": "get_report", "language": "mixed"},
            {"text": "15 February से 15 March के बीच का report बताओ", "intent": "get_report", "language": "mixed"},
            {"text": "1 April से 30 April तक का report", "intent": "get_report", "language": "mixed"},
            {"text": "10 May से 20 May तक का report दिखाओ", "intent": "get_report", "language": "mixed"},
            
            {"text": "Show report from 1 जनवरी to 31 जनवरी", "intent": "get_report", "language": "mixed"},
            {"text": "Get report between 15 फरवरी and 15 मार्च", "intent": "get_report", "language": "mixed"},
            {"text": "Display report for 1 अप्रैल to 30 अप्रैल", "intent": "get_report", "language": "mixed"},
            {"text": "View report from 10 मई to 20 मई", "intent": "get_report", "language": "mixed"},
        ]
        
        print(f"Created {len(self.training_data)} default training examples")
    
    def save_training_data(self, output_path: str) -> None:
        """Save the training data to a file.
        
        Args:
            output_path: Path to save the training data to.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(self.training_data)} training examples to {output_path}")
        except Exception as e:
            print(f"Error saving training data: {e}")
    
    def augment_training_data(self) -> None:
        """Augment the training data with variations of existing examples."""
        original_data = self.training_data.copy()
        augmented_data = []
        
        for example in original_data:
            text = example["text"]
            intent = example["intent"]
            language = example["language"]
            
            # Skip augmentation for mixed language examples to avoid complexity
            if language == "mixed":
                continue
            
            # Simple word substitution for English
            if language == "en":
                # Replace common verbs
                if "show" in text.lower():
                    augmented_data.append({"text": text.lower().replace("show", "display"), "intent": intent, "language": language})
                if "get" in text.lower():
                    augmented_data.append({"text": text.lower().replace("get", "fetch"), "intent": intent, "language": language})
                
                # Add/remove articles and prepositions
                if "the" in text.lower():
                    augmented_data.append({"text": text.lower().replace("the ", ""), "intent": intent, "language": language})
                elif re.search(r'\b(inventory|stock|report|orders)\b', text.lower()):
                    for match in re.finditer(r'\b(inventory|stock|report|orders)\b', text.lower()):
                        word = match.group(1)
                        augmented_data.append({"text": text.lower().replace(word, f"the {word}"), "intent": intent, "language": language})
            
            # Simple word substitution for Hindi
            elif language == "hi":
                # Replace common verbs
                if "दिखाओ" in text:
                    augmented_data.append({"text": text.replace("दिखाओ", "बताओ"), "intent": intent, "language": language})
                if "बताओ" in text:
                    augmented_data.append({"text": text.replace("बताओ", "दिखाओ"), "intent": intent, "language": language})
        
        # Add the augmented examples to the training data
        self.training_data.extend(augmented_data)
        print(f"Augmented training data with {len(augmented_data)} additional examples")
    
    def prepare_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepare the data for training.
        
        Returns:
            Tuple containing X_train, X_test, y_train, y_test.
        """
        # Extract texts and labels
        texts = [example["text"] for example in self.training_data]
        intents = [example["intent"] for example in self.training_data]
        
        # Encode labels
        self.label_encoder.fit(intents)
        y = self.label_encoder.transform(intents)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, model_type: str = "svm") -> None:
        """Train the intent recognition model.
        
        Args:
            model_type: Type of model to train. Options: "svm", "rf" (Random Forest), "nb" (Naive Bayes), "lr" (Logistic Regression).
        """
        X_train, X_test, y_train, y_test = self.prepare_data()
        
        # Create the model based on the specified type
        if model_type == "rf":
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == "nb":
            clf = MultinomialNB()
        elif model_type == "lr":
            clf = LogisticRegression(max_iter=1000, random_state=42)
        else:  # Default to SVM
            clf = LinearSVC()
        
        # Create the pipeline
        self.model = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', clf)
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
        
        print(f"Model trained with accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(report)
    
    def save_model(self, model_path: str, vectorizer_path: str, encoder_path: str) -> None:
        """Save the trained model and associated components.
        
        Args:
            model_path: Path to save the model to.
            vectorizer_path: Path to save the vectorizer to.
            encoder_path: Path to save the label encoder to.
        """
        if self.model is None:
            print("No model to save. Please train a model first.")
            return
        
        try:
            # Save the model
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            # Save the vectorizer
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            # Save the label encoder
            with open(encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            
            print(f"Model saved to {model_path}")
            print(f"Vectorizer saved to {vectorizer_path}")
            print(f"Label encoder saved to {encoder_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self, model_path: str, vectorizer_path: str, encoder_path: str) -> None:
        """Load a trained model and associated components.
        
        Args:
            model_path: Path to load the model from.
            vectorizer_path: Path to load the vectorizer from.
            encoder_path: Path to load the label encoder from.
        """
        try:
            # Load the model
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load the vectorizer
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load the label encoder
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print(f"Model loaded from {model_path}")
            print(f"Vectorizer loaded from {vectorizer_path}")
            print(f"Label encoder loaded from {encoder_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict_intent(self, text: str) -> Tuple[str, float]:
        """Predict the intent of a given text.
        
        Args:
            text: The text to predict the intent for.
            
        Returns:
            Tuple containing the predicted intent and confidence score.
        """
        if self.model is None:
            print("No model available. Please train or load a model first.")
            return "unknown", 0.0
        
        # Predict the intent
        intent_idx = self.model.predict([text])[0]
        intent = self.label_encoder.inverse_transform([intent_idx])[0]
        
        # Get confidence score (if available)
        confidence = 1.0  # Default confidence
        try:
            # For models that support decision_function (e.g., SVM)
            if hasattr(self.model, 'decision_function'):
                confidence_scores = self.model.decision_function([text])[0]
                confidence = confidence_scores[intent_idx]
            # For models that support predict_proba (e.g., Random Forest, Naive Bayes)
            elif hasattr(self.model, 'predict_proba'):
                confidence_scores = self.model.predict_proba([text])[0]
                confidence = confidence_scores[intent_idx]
        except:
            pass
        
        return intent, confidence
    
    def evaluate_model(self, test_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, float]:
        """Evaluate the model on test data.
        
        Args:
            test_data: List of test examples. If None, a portion of the training data will be used.
            
        Returns:
            Dictionary containing evaluation metrics.
        """
        if self.model is None:
            print("No model available. Please train or load a model first.")
            return {}
        
        if test_data is None:
            # Use a portion of the training data for testing
            _, X_test, _, y_test = self.prepare_data()
        else:
            # Use the provided test data
            X_test = [example["text"] for example in test_data]
            intents = [example["intent"] for example in test_data]
            y_test = self.label_encoder.transform(intents)
        
        # Predict intents
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_, output_dict=True)
        
        # Extract metrics from the report
        metrics = {
            "accuracy": accuracy,
            "macro_avg_precision": report["macro avg"]["precision"],
            "macro_avg_recall": report["macro avg"]["recall"],
            "macro_avg_f1": report["macro avg"]["f1-score"],
            "weighted_avg_precision": report["weighted avg"]["precision"],
            "weighted_avg_recall": report["weighted avg"]["recall"],
            "weighted_avg_f1": report["weighted avg"]["f1-score"],
        }
        
        # Add per-intent metrics
        for intent in self.label_encoder.classes_:
            metrics[f"{intent}_precision"] = report[intent]["precision"]
            metrics[f"{intent}_recall"] = report[intent]["recall"]
            metrics[f"{intent}_f1"] = report[intent]["f1-score"]
        
        return metrics
    
    def cross_validate_models(self, n_splits: int = 5) -> Dict[str, Dict[str, float]]:
        """Perform cross-validation on multiple model types.
        
        Args:
            n_splits: Number of cross-validation splits.
            
        Returns:
            Dictionary containing evaluation metrics for each model type.
        """
        from sklearn.model_selection import KFold
        
        # Extract texts and labels
        texts = [example["text"] for example in self.training_data]
        intents = [example["intent"] for example in self.training_data]
        
        # Encode labels
        y = self.label_encoder.transform(intents)
        
        # Initialize KFold
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        # Model types to evaluate
        model_types = {
            "svm": LinearSVC(),
            "rf": RandomForestClassifier(n_estimators=100, random_state=42),
            "nb": MultinomialNB(),
            "lr": LogisticRegression(max_iter=1000, random_state=42)
        }
        
        # Results dictionary
        results = {model_name: {"accuracy": [], "macro_f1": []} for model_name in model_types}
        
        # Perform cross-validation
        for train_idx, test_idx in kf.split(texts):
            X_train = [texts[i] for i in train_idx]
            X_test = [texts[i] for i in test_idx]
            y_train = y[train_idx]
            y_test = y[test_idx]
            
            # Vectorize the text
            X_train_vec = self.vectorizer.fit_transform(X_train)
            X_test_vec = self.vectorizer.transform(X_test)
            
            # Train and evaluate each model
            for model_name, model in model_types.items():
                model.fit(X_train_vec, y_train)
                y_pred = model.predict(X_test_vec)
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                report = classification_report(y_test, y_pred, output_dict=True)
                macro_f1 = report["macro avg"]["f1-score"]
                
                # Store results
                results[model_name]["accuracy"].append(accuracy)
                results[model_name]["macro_f1"].append(macro_f1)
        
        # Calculate average metrics
        for model_name in model_types:
            results[model_name]["avg_accuracy"] = np.mean(results[model_name]["accuracy"])
            results[model_name]["avg_macro_f1"] = np.mean(results[model_name]["macro_f1"])
            results[model_name]["std_accuracy"] = np.std(results[model_name]["accuracy"])
            results[model_name]["std_macro_f1"] = np.std(results[model_name]["macro_f1"])
        
        return results


def main():
    """Main function to demonstrate the model trainer."""
    # Create a model trainer
    trainer = ModelTrainer()
    
    # Augment the training data
    trainer.augment_training_data()
    
    # Save the training data
    trainer.save_training_data("multilingual_training_data.json")
    
    # Train the model
    print("\nTraining SVM model...")
    trainer.train_model(model_type="svm")
    
    # Save the model
    trainer.save_model(
        model_path="multilingual_intent_model.pkl",
        vectorizer_path="multilingual_vectorizer.pkl",
        encoder_path="multilingual_label_encoder.pkl"
    )
    
    # Cross-validate different models
    print("\nPerforming cross-validation...")
    cv_results = trainer.cross_validate_models(n_splits=5)
    
    # Print cross-validation results
    print("\nCross-validation results:")
    for model_name, metrics in cv_results.items():
        print(f"\n{model_name.upper()}:")
        print(f"Average Accuracy: {metrics['avg_accuracy']:.4f} ± {metrics['std_accuracy']:.4f}")
        print(f"Average Macro F1: {metrics['avg_macro_f1']:.4f} ± {metrics['std_macro_f1']:.4f}")
    
    # Test some predictions
    print("\nTesting predictions...")
    test_texts = [
        "Show inventory",
        "इन्वेंटरी दिखाओ",
        "Show कम स्टॉक",
        "Update प्रोडक्ट A का stock, add 10 units",
        "Aaj ke report dikhao",
        "1 जनवरी से 31 जनवरी तक का रिपोर्ट दिखाओ"
    ]
    
    for text in test_texts:
        intent, confidence = trainer.predict_intent(text)
        print(f"Text: {text}")
        print(f"Predicted Intent: {intent}")
        print(f"Confidence: {confidence:.4f}\n")


if __name__ == "__main__":
    main()