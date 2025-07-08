import string
from command_mappings import COMMAND_MAPPINGS


import re
import string
from command_mappings import COMMAND_MAPPINGS


COMMAND_PATTERNS = {
    "add product": ["add product", "i want to add a new product", "create product"],
    "delete product": ["delete product", "remove product", "discard product"],
    "view orders": ["show me my orders", "view orders", "list my orders"],
    "view inventory": ["show me my inventory", "view inventory", "list my inventory"],
    "update stock": ["update stock", "change stock", "modify stock"]
}

def parse_command(message: str):
    # Normalize and parse the message
    normalized_message = message.lower().strip()
    for command, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            if pattern in normalized_message:
                # Extract parameters based on command
                if command == "update stock":
                    parts = normalized_message.split()
                    try:
                        product_id = int(parts[-2])
                        stock = int(parts[-1])
                        return {"action": "update_inventory", "product_id": product_id, "stock": stock}
                    except (ValueError, IndexError):
                        return {"action": "update_inventory", "error": "Invalid format"}
                # Handle other commands
                return {"action": command.replace(" ", "_")}
    return {"action": "unknown"}


# Example usage:
# print(parse_command("Please add product"))
# Output: {'action': 'create_product', 'required_fields': ['name', 'price', 'stock']}