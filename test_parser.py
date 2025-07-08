from parser import parse_command

def test_parser():
    assert parse_command("add product")['action'] == "create_product"
    assert parse_command("please add product now")['action'] == "create_product"
    assert parse_command("i want to add a new product")['action'] == "create_product"
    assert parse_command("create product")['action'] == "create_product"
    assert parse_command("delete product 5")['action'] == "delete_product"
    assert parse_command("remove product 10")['action'] == "delete_product"
    assert parse_command("discard product 3")['action'] == "delete_product"
    assert parse_command("show me my orders")['action'] == "get_orders"
    assert parse_command("view orders")['action'] == "get_orders"
    assert parse_command("list my orders")['action'] == "get_orders"
    assert parse_command("hi")['action'] == "unknown"

test_parser()
print("All tests passed.")