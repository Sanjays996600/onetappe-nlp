from mixed_entity_extraction import extract_mixed_date_range, normalize_mixed_command

# Test cases for basic relative date patterns
test_cases = [
    "7 days ago",
    "7 दिन पहले",
    "7 din pehle",
    "2 weeks ago",
    "2 हफ्ते पहले",
    "3 months ago",
    "3 महीने पहले",
    # Test cases with report suffix
    "7 days ago report",
    "7 दिन पहले से report",
    "report from 7 days ago",
    "7 days ago से report"
]

print("Testing basic relative date patterns:")
print("-" * 50)

for cmd in test_cases:
    # First normalize the command
    normalized_cmd = normalize_mixed_command(cmd)
    
    # Extract date range
    result = extract_mixed_date_range(normalized_cmd)
    
    # Format output
    print(f"Command: {cmd}")
    print(f"Normalized: '{normalized_cmd}'")
    if result and result.get("period"):
        print(f"Result: {result.get('period')}")
    else:
        print("Result: Not detected")
    print("-" * 50)