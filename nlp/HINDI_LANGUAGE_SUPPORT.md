# Hindi Language Support Implementation Guide

This document provides detailed guidance for implementing and improving Hindi language support in the multilingual NLP chatbot system.

## Overview

Hindi language support is a critical component of our multilingual NLP system, enabling the chatbot to understand and respond to commands in Hindi. This guide covers the implementation details, challenges, and best practices for Hindi language processing.

## Hindi Language Characteristics

### Script and Character Set

Hindi uses the Devanagari script, which includes:

- Vowels (अ, आ, इ, ई, उ, ऊ, ए, ऐ, ओ, औ)
- Consonants (क, ख, ग, घ, etc.)
- Matras (vowel signs: ा, ि, ी, ु, ू, etc.)
- Numerals (०, १, २, ३, etc.)
- Special characters (ं, ः, ँ, etc.)

The Unicode range for Devanagari is U+0900 to U+097F.

### Linguistic Challenges

1. **Word Order**: Hindi typically follows Subject-Object-Verb (SOV) order, unlike English's Subject-Verb-Object (SVO)
2. **Gender and Number Agreement**: Hindi has grammatical gender and number agreement
3. **Case Marking**: Hindi uses postpositions instead of prepositions
4. **Honorifics**: Different levels of formality and respect
5. **Compound Words**: Frequent use of compound words

## Implementation Components

### 1. Character Recognition and Normalization

```python
# Define Hindi character range
HINDI_CHAR_RANGE = r'[\u0900-\u097F]'

# Function to normalize Hindi text
def normalize_hindi_text(text):
    # Remove unnecessary spaces
    text = re.sub(r'\s+', ' ', text)
    # Normalize Unicode representations
    text = unicodedata.normalize('NFC', text)
    return text.strip()
```

### 2. Hindi Intent Patterns

Define regex patterns for recognizing intents in Hindi:

```python
HINDI_INTENT_PATTERNS = {
    "get_inventory": [
        r"(मेरा|हमारा)\s+(इन्वेंटरी|इन्वेंट्री|स्टॉक|सामान|प्रोडक्ट्स?)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए)",
        r"(स्टॉक|इन्वेंटरी|इन्वेंट्री|सामान|प्रोडक्ट्स?)\s+(कितना|क्या|कौन सा)\s+(है|हैं|बचा है|बचे हैं)",
        r"(सभी|सारे)\s+(प्रोडक्ट्स?|आइटम्स?|सामान|वस्तुएं)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए)"
    ],
    "get_low_stock": [
        r"(कम|लो)\s+(स्टॉक|इन्वेंटरी)\s+(वाले|वाला)\s+(प्रोडक्ट्स?|आइटम्स?|सामान)",
        r"(कौन\s+से|कौन\s+सा)\s+(प्रोडक्ट्स?|आइटम्स?|सामान)\s+(कम|लो)\s+(है|हैं|हो\s+रहा\s+है|हो\s+रहे\s+हैं)",
        r"(कम|लो)\s+(स्टॉक|इन्वेंटरी)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए)"
    ],
    "get_report": [
        r"(रिपोर्ट|सेल्स|बिक्री|परफॉरमेंस)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए|जनरेट करें|जनरेट करो|बनाओ)",
        r"(पिछले|इस)\s+(हफ्ते|महीने|साल|दिन|सप्ताह)\s+(की|का)\s+(रिपोर्ट|सेल्स|बिक्री)",
        r"(जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर)\s+(की|का)\s+(रिपोर्ट|सेल्स|बिक्री)"
    ],
    "edit_stock": [
        r"([\w\s]+)\s+(का|की)\s+(स्टॉक|इन्वेंटरी)\s+([0-9]+)\s+(करो|करें|अपडेट करो|अपडेट करें|सेट करो|सेट करें)",
        r"([\w\s]+)\s+(स्टॉक|इन्वेंटरी)\s+([0-9]+)\s+(में|को)\s+(बदलो|बदलें|अपडेट करो|अपडेट करें)",
        r"([\w\s]+)\s+(की|का)\s+(मात्रा|क्वांटिटी)\s+([0-9]+)\s+(करो|करें|सेट करो|सेट करें)"
    ],
    "get_orders": [
        r"(ऑर्डर्स?|आर्डर्स?|ऑर्डर|आर्डर)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए)",
        r"(पिछले|हाल के|रीसेंट)\s+(ऑर्डर्स?|आर्डर्स?|ऑर्डर|आर्डर)\s+(दिखाओ|दिखाएं|देखना|देखना है|चाहिए)",
        r"(पिछले|इस)\s+(हफ्ते|महीने|साल|दिन|सप्ताह)\s+(के|की|का)\s+(ऑर्डर्स?|आर्डर्स?|ऑर्डर|आर्डर)"
    ],
    "search_product": [
        r"([\w\s]+)\s+(प्रोडक्ट्स?|आइटम्स?|सामान)\s+(खोजो|खोजें|सर्च करो|सर्च करें|ढूंढो|ढूंढें)",
        r"([\w\s]+)\s+(के लिए|की)\s+(खोज|सर्च)\s+(करो|करें)",
        r"(इन्वेंटरी|स्टॉक)\s+में\s+([\w\s]+)\s+(खोजो|खोजें|सर्च करो|सर्च करें|ढूंढो|ढूंढें)"
    ]
}
```

### 3. Entity Extraction for Hindi

Implement entity extraction functions for Hindi commands:

```python
def extract_product_name_hindi(text, intent):
    """Extract product name from Hindi text based on intent."""
    if intent == "edit_stock":
        match = re.search(r"([\w\s]+)\s+(का|की)\s+(स्टॉक|इन्वेंटरी)", text)
        if match:
            return match.group(1).strip()
    elif intent == "search_product":
        match = re.search(r"([\w\s]+)\s+(प्रोडक्ट्स?|आइटम्स?|सामान)\s+(खोजो|खोजें|सर्च)", text)
        if match:
            return match.group(1).strip()
    return None

def extract_quantity_hindi(text):
    """Extract quantity from Hindi text."""
    # Look for number followed by optional unit
    match = re.search(r"([0-9]+)\s*(किलो|किग्रा|ग्राम|पीस|पैकेट|लीटर)?", text)
    if match:
        return int(match.group(1))
    return None

def extract_time_period_hindi(text):
    """Extract time period from Hindi text."""
    if re.search(r"पिछले\s+हफ्ते", text):
        return "last_week"
    elif re.search(r"इस\s+हफ्ते", text):
        return "this_week"
    elif re.search(r"पिछले\s+महीने", text):
        return "last_month"
    elif re.search(r"इस\s+महीने", text):
        return "this_month"
    elif re.search(r"हाल\s+के|रीसेंट", text):
        return "recent"
    # Add more time period patterns
    return None
```

### 4. Response Templates for Hindi

Create response templates for generating Hindi responses:

```python
HINDI_RESPONSE_TEMPLATES = {
    "get_inventory": "आपका वर्तमान इन्वेंटरी:\n{inventory_list}",
    "get_low_stock": "कम स्टॉक वाले प्रोडक्ट्स:\n{low_stock_list}",
    "get_report": "{time_period} की रिपोर्ट:\n{report_data}",
    "edit_stock": "{product_name} का स्टॉक {stock} अपडेट किया गया",
    "get_orders": "{time_period} के ऑर्डर्स:\n{orders_list}",
    "search_product": "{product_name} के लिए खोज परिणाम:\n{search_results}",
    "error": "क्षमा करें, मैं आपके अनुरोध को समझ नहीं पाया। कृपया दोबारा प्रयास करें।"
}
```

### 5. Hindi Number and Date Formatting

Implement functions for formatting numbers and dates in Hindi:

```python
def format_number_hindi(number):
    """Format number in Hindi style."""
    # Convert to Hindi numerals if needed
    # For now, just return as string
    return str(number)

def format_date_hindi(date_obj):
    """Format date in Hindi style."""
    hindi_months = [
        "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून",
        "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
    ]
    return f"{date_obj.day} {hindi_months[date_obj.month-1]} {date_obj.year}"
```

## Mixed Language Support

### 1. Detecting Mixed Language Input

```python
def detect_mixed_language(text, threshold=0.3):
    """Detect if text contains significant portions of both English and Hindi."""
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return False
    
    hindi_ratio = hindi_chars / total_chars
    english_ratio = english_chars / total_chars
    
    # Text is considered mixed if both languages have significant presence
    return hindi_ratio > threshold and english_ratio > threshold
```

### 2. Handling Mixed Language Commands

```python
def handle_mixed_language_input(text):
    """Process mixed language input by segmenting and analyzing each part."""
    # Segment text into Hindi and English parts
    hindi_segments = re.findall(f"({HINDI_CHAR_RANGE}+\s*)+", text)
    english_segments = re.findall(f"({ENGLISH_CHAR_RANGE}+\s*)+", text)
    
    # Try to detect intent using both languages
    intent = None
    entities = {}
    
    # First try with full text in both languages
    intent = detect_intent(text, "en") or detect_intent(text, "hi")
    
    if not intent:
        # Try with individual segments
        for segment in hindi_segments:
            intent = detect_intent(segment, "hi")
            if intent:
                break
        
        if not intent:
            for segment in english_segments:
                intent = detect_intent(segment, "en")
                if intent:
                    break
    
    # Extract entities based on detected intent
    if intent:
        # Try extracting from full text first
        entities = extract_entities(text, intent, "mixed")
        
        # If specific entities are missing, try language-specific extraction
        if not entities.get("product_name") and intent in ["edit_stock", "search_product"]:
            for segment in hindi_segments:
                product_name = extract_product_name_hindi(segment, intent)
                if product_name:
                    entities["product_name"] = product_name
                    break
            
            if not entities.get("product_name"):
                for segment in english_segments:
                    product_name = extract_product_name_english(segment, intent)
                    if product_name:
                        entities["product_name"] = product_name
                        break
    
    return {
        "intent": intent,
        "entities": entities,
        "is_mixed_language": True
    }
```

## Transliteration Support

Implement transliteration support for handling Hindi written in Latin script (Hinglish):

```python
def detect_transliterated_hindi(text):
    """Detect if text is likely Hindi transliterated in Latin script (Hinglish)."""
    # Common Hinglish patterns
    hinglish_patterns = [
        r"\b(kya|kaise|kitna|kaun|kahan)\b",  # Question words
        r"\b(hai|hain|tha|thi|the|hoga|hogi)\b",  # Forms of "to be"
        r"\b(mera|meri|mujhe|humara|humari|hume)\b",  # Possessives
        r"\b(aur|ya|lekin|par|ki|ka|ke)\b",  # Conjunctions and postpositions
        r"\b(dekho|dikhao|karo|karein|do|dijiye)\b"  # Common verbs
    ]
    
    # Check for presence of Hinglish patterns
    hinglish_matches = sum(1 for pattern in hinglish_patterns if re.search(pattern, text.lower()))
    
    # If multiple Hinglish patterns are found, it's likely transliterated Hindi
    return hinglish_matches >= 2

def map_transliterated_intent(text):
    """Map transliterated Hindi (Hinglish) to intents."""
    # Patterns for common transliterated Hindi commands
    transliterated_patterns = {
        "get_inventory": [
            r"\b(mera|hamara)\s+(inventory|stock|samaan|products?)\s+(dikhao|dikhaiye|dekhna)\b",
            r"\b(stock|inventory|samaan|products?)\s+(kitna|kya|kaun sa)\s+(hai|hain|bacha hai|bache hain)\b"
        ],
        "get_low_stock": [
            r"\b(kam|low)\s+(stock|inventory)\s+(wale|wala)\s+(products?|items?|samaan)\b",
            r"\b(kaun\s+se|kaun\s+sa)\s+(products?|items?|samaan)\s+(kam|low)\s+(hai|hain|ho\s+raha\s+hai|ho\s+rahe\s+hain)\b"
        ],
        # Add more transliterated patterns for other intents
    }
    
    # Check for matches in transliterated patterns
    for intent, patterns in transliterated_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return intent
    
    return None
```

## Improving Hindi Language Support

### 1. Expanding Vocabulary

Continuously expand the vocabulary and patterns for Hindi commands:

```python
# Add synonyms for common terms
HINDI_PRODUCT_SYNONYMS = {
    "चावल": ["राइस", "चावल", "चावल के दाने"],
    "गेहूं": ["गेहूँ", "गेहू", "गेहूं का आटा", "आटा"],
    "दाल": ["दाल", "पल्स", "दालें"],
    "चीनी": ["चीनी", "शुगर", "शक्कर"],
    "तेल": ["तेल", "ऑयल", "रिफाइंड तेल"]
}

# Add more time-related terms
HINDI_TIME_TERMS = {
    "day": ["दिन", "दिवस"],
    "week": ["हफ्ता", "सप्ताह", "वीक"],
    "month": ["महीना", "माह", "मंथ"],
    "year": ["साल", "वर्ष", "ईयर"],
    "yesterday": ["कल", "बीता हुआ दिन", "पिछला दिन"],
    "today": ["आज", "वर्तमान दिन"],
    "tomorrow": ["कल", "अगला दिन"],
    "last": ["पिछला", "बीता हुआ", "गत"],
    "this": ["इस", "वर्तमान", "चालू"],
    "next": ["अगला", "आने वाला"]
}
```

### 2. Handling Dialectal Variations

Implement support for different Hindi dialects and regional variations:

```python
def normalize_hindi_dialectal_variations(text):
    """Normalize dialectal variations in Hindi text."""
    # Map common dialectal variations to standard forms
    dialectal_mappings = {
        r"हमको": "हमें",
        r"तुमको": "तुम्हें",
        r"करेगा": "करेगा",
        r"करेंगे": "करेंगे",
        # Add more mappings as needed
    }
    
    for variant, standard in dialectal_mappings.items():
        text = re.sub(r"\b" + variant + r"\b", standard, text)
    
    return text
```

### 3. Improving Entity Recognition

Enhance entity recognition for Hindi using contextual clues:

```python
def extract_entities_with_context(text, intent, language="hi"):
    """Extract entities with contextual awareness."""
    entities = {}
    
    if intent == "edit_stock":
        # Look for product name followed by quantity
        match = re.search(r"([\w\s]+)\s+(का|की)\s+(स्टॉक|इन्वेंटरी)\s+([0-9]+)", text)
        if match:
            entities["product_name"] = match.group(1).strip()
            entities["stock"] = int(match.group(4))
        
        # Look for quantity unit if present
        unit_match = re.search(r"([0-9]+)\s+(किलो|किग्रा|ग्राम|पीस|पैकेट|लीटर)", text)
        if unit_match:
            entities["unit"] = unit_match.group(2)
    
    # Add more intent-specific entity extraction with context
    
    return entities
```

## Testing Hindi Language Support

### 1. Test Cases for Hindi Commands

Create comprehensive test cases for Hindi commands:

```python
HINDI_TEST_CASES = [
    # Get inventory tests
    {"text": "मेरा इन्वेंटरी दिखाओ", "intent": "get_inventory", "entities": {}},
    {"text": "सभी प्रोडक्ट्स की लिस्ट दिखाएं", "intent": "get_inventory", "entities": {}},
    {"text": "स्टॉक कितना बचा है", "intent": "get_inventory", "entities": {}},
    
    # Get low stock tests
    {"text": "कम स्टॉक वाले आइटम दिखाओ", "intent": "get_low_stock", "entities": {}},
    {"text": "कौन से प्रोडक्ट्स कम हो रहे हैं", "intent": "get_low_stock", "entities": {}},
    
    # Edit stock tests
    {"text": "चावल का स्टॉक 50 किलो अपडेट करें", "intent": "edit_stock", "entities": {"product_name": "चावल", "stock": 50, "unit": "किलो"}},
    {"text": "गेहूं की मात्रा 75 सेट करो", "intent": "edit_stock", "entities": {"product_name": "गेहूं", "stock": 75}},
    
    # Get report tests
    {"text": "पिछले हफ्ते की बिक्री रिपोर्ट जनरेट करें", "intent": "get_report", "entities": {"time_period": "last_week"}},
    {"text": "इस महीने की रिपोर्ट दिखाएं", "intent": "get_report", "entities": {"time_period": "this_month"}},
    
    # Get orders tests
    {"text": "मेरे हाल के ऑर्डर दिखाएं", "intent": "get_orders", "entities": {"time_period": "recent"}},
    {"text": "पिछले हफ्ते के ऑर्डर दिखाओ", "intent": "get_orders", "entities": {"time_period": "last_week"}},
    
    # Search product tests
    {"text": "चावल प्रोडक्ट्स के लिए खोजें", "intent": "search_product", "entities": {"product_name": "चावल"}},
    {"text": "इन्वेंटरी में दाल खोजो", "intent": "search_product", "entities": {"product_name": "दाल"}}
]
```

### 2. Test Function for Hindi Support

Implement a test function for evaluating Hindi language support:

```python
def test_hindi_support():
    """Test Hindi language support functionality."""
    correct_intent = 0
    correct_entities = 0
    total_tests = len(HINDI_TEST_CASES)
    
    for test_case in HINDI_TEST_CASES:
        text = test_case["text"]
        expected_intent = test_case["intent"]
        expected_entities = test_case["entities"]
        
        # Detect language
        detected_lang, _ = detect_language_with_confidence(text)
        
        # Parse command
        parsed = parse_multilingual_command(text)
        detected_intent = parsed.get("intent", "")
        detected_entities = parsed.get("entities", {})
        
        # Check intent accuracy
        if detected_intent == expected_intent:
            correct_intent += 1
        
        # Check entity extraction accuracy
        entities_correct = True
        for key, value in expected_entities.items():
            if key not in detected_entities or detected_entities[key] != value:
                entities_correct = False
                break
        
        if entities_correct:
            correct_entities += 1
        
        print(f"Test: {text}")
        print(f"Language: {detected_lang}")
        print(f"Intent: {detected_intent} (Expected: {expected_intent})")
        print(f"Entities: {detected_entities}")
        print(f"Entities Correct: {entities_correct}")
        print("---")
    
    intent_accuracy = correct_intent / total_tests
    entity_accuracy = correct_entities / total_tests
    
    print(f"Hindi Intent Recognition Accuracy: {intent_accuracy:.2f}")
    print(f"Hindi Entity Extraction Accuracy: {entity_accuracy:.2f}")
    
    return intent_accuracy, entity_accuracy
```

## Best Practices for Hindi NLP

### 1. Text Preprocessing

- **Normalization**: Normalize Unicode representations to handle different encoding variations
- **Tokenization**: Use specialized tokenizers for Hindi that handle compound words and affixes
- **Stemming**: Apply Hindi-specific stemming to reduce words to their root forms

### 2. Entity Recognition

- **Named Entity Recognition**: Use specialized NER models trained on Hindi data
- **Dictionary-Based Approach**: Maintain dictionaries of common Hindi terms for products, actions, etc.
- **Context-Aware Extraction**: Consider the surrounding context when extracting entities

### 3. Intent Recognition

- **Hybrid Approach**: Combine rule-based patterns with ML models
- **Contextual Understanding**: Consider previous messages for context
- **Confidence Scoring**: Implement confidence scores for intent recognition

### 4. Response Generation

- **Grammatical Correctness**: Ensure responses follow Hindi grammar rules
- **Formality Levels**: Support different levels of formality based on user preferences
- **Natural Phrasing**: Use natural Hindi phrasing rather than direct translations from English

## Integration with ML Models

### 1. Hindi-Specific Word Embeddings

```python
def load_hindi_embeddings():
    """Load pre-trained Hindi word embeddings."""
    try:
        # Load fastText Hindi embeddings
        from gensim.models import KeyedVectors
        hindi_embeddings = KeyedVectors.load_word2vec_format('cc.hi.300.vec')
        return hindi_embeddings
    except Exception as e:
        print(f"Error loading Hindi embeddings: {e}")
        return None
```

### 2. Fine-tuning Transformer Models for Hindi

```python
def fine_tune_hindi_model(training_data, model_name="ai4bharat/indic-bert"):
    """Fine-tune a transformer model for Hindi NLP tasks."""
    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
        import torch
        
        # Load pre-trained model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(INTENT_CLASSES))
        
        # Prepare training data
        # ...
        
        # Define training arguments
        training_args = TrainingArguments(
            output_dir="./hindi_intent_model",
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
        )
        
        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset
        )
        
        # Train the model
        trainer.train()
        
        # Save the model
        model.save_pretrained("./hindi_intent_model")
        tokenizer.save_pretrained("./hindi_intent_model")
        
        return True
    except Exception as e:
        print(f"Error fine-tuning Hindi model: {e}")
        return False
```

## Conclusion

Implementing robust Hindi language support requires attention to linguistic details, comprehensive pattern recognition, and continuous improvement based on user feedback. By following the guidelines and implementing the code examples in this document, you can create a multilingual NLP chatbot that effectively understands and responds to Hindi commands.

Key takeaways:

1. **Understand Hindi Linguistic Features**: Pay attention to word order, gender agreement, and other Hindi-specific linguistic features
2. **Comprehensive Pattern Recognition**: Develop extensive regex patterns for intent recognition in Hindi
3. **Context-Aware Entity Extraction**: Extract entities with awareness of surrounding context
4. **Mixed Language Support**: Implement robust handling of mixed language inputs
5. **Continuous Improvement**: Regularly update patterns and vocabulary based on user interactions

By implementing these recommendations, you can create a chatbot that provides a natural and effective user experience for Hindi-speaking users.