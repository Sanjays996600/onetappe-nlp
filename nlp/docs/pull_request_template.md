# Pull Request: Add Support for 'Current Stock' Pattern

## Description

This PR adds support for the 'current stock' pattern in the intent recognition system. The pattern is designed to match user queries about viewing their current inventory.

## Changes

1. Added new regex patterns to the `get_inventory` intent in `intent_handler.py` to match 'current stock' queries
2. Added support for Hindi transliteration of 'stock' as 'स्टॉक'
3. Added support for variations with different spacing and punctuation
4. Created comprehensive test cases in `test_current_stock_pattern.py`
5. Added documentation in `docs/current_stock_pattern.md`

## Testing

The changes have been tested with:

- Basic pattern tests with various commands using the 'current stock' pattern
- Variations with different prefixes and suffixes
- Edge cases including different capitalizations, spacing, and punctuation

## Related Issues

Resolves issue #XXX: Add support for 'current stock' pattern

## Checklist

- [x] Code follows the project's coding style
- [x] Tests have been added/updated
- [x] Documentation has been added/updated
- [x] All tests pass