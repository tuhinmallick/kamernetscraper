import unittest
from scraper import parse_room

class TestParseRoom(unittest.TestCase):
    def test_parse_room(self):
        # Test a valid link
        data = parse_room("https://kamernet.nl/huren/kamer-amsterdam-1013-ca")
        self.assertIsInstance(data, dict)
        self.assertIn("streetCityName", data)
        self.assertIn("surfaceArea", data)
        self.assertIn("price", data)
        self.assertIn("unit", data)
        self.assertIn("deliveryLevel", data)
        self.assertIn("availability", data)

        # Test an invalid link
        data = parse_room("https://kamernet.nl/huren/kamers-nederland/invalid")
        self.assertEqual(data, {})

if __name__ == '__main__':
    unittest.main()
