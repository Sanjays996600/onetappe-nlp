import unittest
from auth.utils import extract_category_pincode, find_sellers

class TestUtils(unittest.TestCase):

    def test_extract_category_pincode(self):
        message = "I need an electrician in 827001"
        category, pincode = extract_category_pincode(message)
        self.assertEqual(category, "electrician")
        self.assertEqual(pincode, "827001")

    def test_find_sellers(self):
        sellers = find_sellers("electrician", "827001")
        self.assertGreater(len(sellers), 0)
        self.assertEqual(sellers[0]["category"], "electrician")
        self.assertEqual(sellers[0]["pincode"], "827001")

if __name__ == '__main__':
    unittest.main()