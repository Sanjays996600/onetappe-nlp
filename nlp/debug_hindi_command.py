import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.hindi_support import parse_hindi_command, extract_hindi_custom_date_range, parse_hindi_date

# Test Hindi commands
commands = [
    "1 जून से 20 जून तक की रिपोर्ट दिखाओ",
    "रिपोर्ट दिखाओ 1 जनवरी से 31 जनवरी तक"
]

for command in commands:
    print("\n" + "-"*50)
    print(f"Testing command: '{command}'")
    
    # Test direct extraction
    print("\nDirect extraction:")
    custom_range = extract_hindi_custom_date_range(command)
    print(f"Custom range result: {custom_range}")
    
    # Test full parsing
    print("\nFull command parsing:")
    result = parse_hindi_command(command)
    print(f"Intent: {result['intent']}")
    print(f"Language: {result['language']}")
    print(f"Entities: {result['entities']}")
    
    # Test date parsing directly
    print("\nDirect date parsing:")
    if "जून" in command:
        print("Parsing '1 जून':")
        date = parse_hindi_date("1 जून")
        print(f"Result: {date}")
        
        print("\nParsing '20 जून':")
        date = parse_hindi_date("20 जून")
        print(f"Result: {date}")
    
    if "जनवरी" in command:
        print("\nParsing '1 जनवरी':")
        date = parse_hindi_date("1 जनवरी")
        print(f"Result: {date}")
        
        print("\nParsing '31 जनवरी':")
        date = parse_hindi_date("31 जनवरी")
        print(f"Result: {date}")