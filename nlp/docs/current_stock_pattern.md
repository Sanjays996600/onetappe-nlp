# Current Stock Pattern Implementation

## Overview

This document describes the implementation of the 'current stock' pattern in the intent recognition system. The pattern is designed to match user queries about viewing their current inventory.

## Pattern Definition

The 'current stock' pattern is defined in `intent_handler.py` as part of the `get_inventory` intent patterns. The pattern is designed to match various forms of queries about current stock, including:

- Simple queries: "current stock"
- Prefixed queries: "show current stock", "check current stock"
- Variations with different spacing and punctuation: "current-stock", "current.stock"

## Implementation Details

### Pattern Regex

The pattern is implemented using the following regex patterns:

```python
r"current\s*[-\.]?\s*stock"
r"current\s*[-\.]?\s*स्टॉक"
r"show\s+current\s*[-\.]?\s*स्टॉक"
r"check\s+current\s*[-\.]?\s*स्टॉक"
r"display\s+current\s*[-\.]?\s*स्टॉक"
```

These patterns account for:
- The word "current" followed by "stock"
- Optional spacing, hyphens, or periods between "current" and "stock"
- Hindi transliteration of "stock" as "स्टॉक"
- Common prefixes like "show", "check", and "display"

### Normalization Handling

The system uses a normalization process that converts certain English words to their Hindi equivalents. For example, "stock" is converted to "स्टॉक" during normalization. The patterns are designed to match both the original English words and their normalized Hindi equivalents.

## Testing

The implementation is tested in `test_current_stock_pattern.py`, which includes:

1. Basic pattern tests with various commands using the 'current stock' pattern
2. Variations with different prefixes and suffixes
3. Edge cases including different capitalizations, spacing, and punctuation

## Future Improvements

1. Add support for more variations of the 'current stock' pattern
2. Improve the normalization process to handle more complex mixed-language queries
3. Add support for more languages beyond English and Hindi