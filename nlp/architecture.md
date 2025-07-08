# One Tappe NLP System Architecture

## System Flow Diagram

```
+-------------------+
|                   |
|  WhatsApp User    |  "Add new product Rice 50rs 20qty"
|                   |
+--------+---------+
         |
         v
+--------+---------+
|                   |
|  WhatsApp Bot     |  Receives user message
|                   |
+--------+---------+
         |
         v
+--------+---------+
|                   |
|  Language         |  Detects language (English/Hindi)
|  Detection        |
|                   |
+--------+---------+
         |
         v
+--------+---------+     +-------------------+
|                   |     |                   |
|  Intent           +---->+  Hindi Intent     |
|  Recognition      |     |  Recognition      |
|  (English)        |     |                   |
+--------+---------+     +--------+----------+
         |                        |
         v                        v
+--------+---------+     +--------+----------+
|                   |     |                   |
|  Entity           |     |  Entity           |
|  Extraction       |     |  Extraction       |
|  (English)        |     |  (Hindi)          |
+--------+---------+     +--------+----------+
         |                        |
         v                        v
+--------+---------+     +--------+----------+
|                   |     |                   |
|  Parsed Result    |     |  Parsed Result    |
|  (English)        |     |  (Hindi)          |
|                   |     |                   |
+--------+---------+     +--------+----------+
         |                        |
         +------------+----------+
                      |
                      v
             +--------+---------+
             |                   |
             |  Command Router   |  Maps intent to API endpoint
             |                   |
             +--------+---------+
                      |
                      v
             +--------+---------+
             |                   |
             |  Backend API      |  Processes the command
             |                   |
             +--------+---------+
                      |
                      v
             +--------+---------+
             |                   |
             |  Response         |  Formats response in user's language
             |  Formatter        |
             |                   |
             +--------+---------+
                      |
                      v
+-------------------+ |
|                   | |
|  WhatsApp User    |<+  "Product Rice added successfully with price ₹50 and stock 20."
|                   |
+-------------------+
```

## Component Interactions

1. **User Input**: The user sends a natural language command via WhatsApp.

2. **Language Detection**: The system detects whether the command is in English or Hindi.

3. **Intent Recognition**: Based on the detected language, the appropriate intent recognition module processes the command.

4. **Entity Extraction**: The system extracts relevant entities (product name, price, stock, etc.) from the command.

5. **Command Routing**: The parsed intent and entities are mapped to the appropriate backend API endpoint.

6. **API Processing**: The backend API processes the command and returns a response.

7. **Response Formatting**: The response is formatted in the user's language and sent back to the user.

## Data Flow Example

### English Command

```
Input: "Add new product Rice 50rs 20qty"

Language Detection: "en"

Intent Recognition: "add_product"

Entity Extraction: {
  "name": "Rice",
  "price": 50,
  "stock": 20
}

Command Routing: POST /seller/products/add

API Request Body: {
  "name": "Rice",
  "price": 50,
  "stock": 20
}

API Response: {
  "success": true,
  "product": {
    "id": "123",
    "name": "Rice",
    "price": 50,
    "stock": 20
  }
}

Formatted Response: "Product Rice added successfully with price ₹50 and stock 20."
```

### Hindi Command

```
Input: "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो"

Language Detection: "hi"

Intent Recognition: "add_product"

Entity Extraction: {
  "name": "चावल",
  "price": 50,
  "stock": 20
}

Command Routing: POST /seller/products/add

API Request Body: {
  "name": "चावल",
  "price": 50,
  "stock": 20
}

API Response: {
  "success": true,
  "product": {
    "id": "124",
    "name": "चावल",
    "price": 50,
    "stock": 20
  }
}

Formatted Response: "प्रोडक्ट चावल को ₹50 कीमत और 20 स्टॉक के साथ सफलतापूर्वक जोड़ा गया।"
```