COMMAND_MAPPINGS = {
    "add product": {
        "action": "create_product",
        "required_fields": ["name", "price", "stock"]
    },
    "edit product": {
        "action": "edit_product",
        "required_fields": ["product_id", "name", "price", "stock"]
    },
    "delete product": {
        "action": "delete_product",
        "required_fields": ["product_id"]
    },
    "view orders": {
        "action": "get_orders",
        "required_fields": []
    },
    "view inventory": {
        "action": "view_inventory",
        "required_fields": []
    },
    "update stock": {
        "action": "update_inventory",
        "required_fields": ["product_id", "stock"]
    }
}