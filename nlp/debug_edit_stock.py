from mixed_entity_extraction import extract_mixed_edit_stock_details, normalize_mixed_command

# Debug the failing test cases
def debug_test_cases():
    # Test case 1: "edit stock of rice to 10kg"
    command1 = "edit stock of rice to 10kg"
    normalized1 = normalize_mixed_command(command1)
    print(f"Original: {command1}")
    print(f"Normalized: {normalized1}")
    result1 = extract_mixed_edit_stock_details(command1)
    print(f"Result: {result1}\n")
    
    # Test case 2: "update the stock of 2kg sugar to 7kg"
    command2 = "update the stock of 2kg sugar to 7kg"
    normalized2 = normalize_mixed_command(command2)
    print(f"Original: {command2}")
    print(f"Normalized: {normalized2}")
    result2 = extract_mixed_edit_stock_details(command2)
    print(f"Result: {result2}\n")

if __name__ == "__main__":
    debug_test_cases()