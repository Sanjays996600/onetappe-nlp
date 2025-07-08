import sys
import os
import json

# Add the parent directory to sys.path to import the intent_handler module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.intent_handler import parse_command, detect_language

def test_intent_recognition():
    """
    Test the intent recognition functionality with various commands
    """
    test_cases = [
        # Basic inventory commands
        "Show my products",
        "List all products",
        "View inventory",
        
        # Report commands with different time ranges
        "Send today's report",
        "Get this week's report",
        "Show this month's report",
        "Generate report",
        
        # Low stock commands
        "Show low stock items",
        "List products with low stock",
        "What items are running low?",
        
        # Add product commands with different formats
        "Add new product Rice 50rs 20qty",
        "Add product Wheat 75 30",
        "Create product Sugar 25rs 15units",
        "Register new product Salt 10 50",
        
        # Edit stock commands
        "Edit stock of Rice to 100",
        "Update Wheat stock to 75",
        "Change stock of Sugar to 50",
        "Set stock of Salt to 25",
        
        # Order commands
        "Show my orders",
        "List recent orders",
        "View all orders",
        
        # Edge cases and potential misunderstandings
        "How many products do I have?",
        "I want to add a new product",
        "Can you update my inventory?",
        "Hello",
        "What can you do?"
    ]
    
    print("\n===== INTENT RECOGNITION TEST =====\n")
    
    for i, command in enumerate(test_cases, 1):
        result = parse_command(command)
        language = detect_language(command)
        
        print(f"Test #{i}: '{command}'")
        print(f"Language: {language}")
        print(f"Intent: {result['intent']}")
        print(f"Entities: {json.dumps(result['entities'], indent=2)}")
        print("-" * 50)

def test_hindi_commands():
    """
    Test basic Hindi commands (placeholder for future Hindi support)
    """
    hindi_test_cases = [
        "मेरे प्रोडक्ट दिखाओ",  # Show my products
        "आज की रिपोर्ट भेजो",    # Send today's report
        "कम स्टॉक वाले आइटम दिखाओ"  # Show low stock items
    ]
    
    print("\n===== HINDI LANGUAGE DETECTION TEST =====\n")
    
    for command in hindi_test_cases:
        language = detect_language(command)
        print(f"Command: '{command}'")
        print(f"Detected Language: {language}")
        print("-" * 50)

def test_complex_scenarios():
    """
    Test more complex scenarios and edge cases
    """
    complex_cases = [
        # Mixed commands
        "Show my products and send today's report",
        "Add Rice 50rs and update Wheat to 75",
        
        # Commands with typos
        "Shw my prodcts",
        "Add prodct Rice 50 20",
        
        # Commands with extra information
        "Show my products please, I need to check inventory",
        "Add new product Rice at 50rs with 20 in stock"
    ]
    
    print("\n===== COMPLEX SCENARIOS TEST =====\n")
    
    for command in complex_cases:
        result = parse_command(command)
        print(f"Command: '{command}'")
        print(f"Intent: {result['intent']}")
        print(f"Entities: {json.dumps(result['entities'], indent=2)}")
        print("-" * 50)

if __name__ == "__main__":
    # Run all tests
    test_intent_recognition()
    test_hindi_commands()
    test_complex_scenarios()
    
    print("\n===== INTERACTIVE TEST MODE =====\n")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nEnter a command: ")
        if user_input.lower() == 'exit':
            break
            
        result = parse_command(user_input)
        language = detect_language(user_input)
        
        print(f"Language: {language}")
        print(f"Intent: {result['intent']}")
        print(f"Entities: {json.dumps(result['entities'], indent=2)}")