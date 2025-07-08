import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.intent_handler import extract_custom_date_range, parse_command
from nlp.hindi_support import extract_hindi_custom_date_range, parse_hindi_command

# Test English commands
english_commands = [
    "Get report from 1 June to 20 June",
    "Get report between 1st January and 31st January",
    "Get report from 01/06 to 20/06"
]

print("\nTesting English custom date range extraction:\n")
for cmd in english_commands:
    print(f"Command: '{cmd}'")
    custom_range = extract_custom_date_range(cmd)
    print(f"Custom range: {custom_range}")
    result = parse_command(cmd)
    print(f"Parse result: {result}\n")

# Test Hindi commands
hindi_commands = [
    "1 जून से 20 जून तक की रिपोर्ट दिखाओ",
    "रिपोर्ट दिखाओ 1 जनवरी से 31 जनवरी तक"
]

print("\nTesting Hindi custom date range extraction:\n")
for cmd in hindi_commands:
    print(f"Command: '{cmd}'")
    custom_range = extract_hindi_custom_date_range(cmd)
    print(f"Custom range: {custom_range}")
    result = parse_hindi_command(cmd)
    print(f"Parse result: {result}\n")