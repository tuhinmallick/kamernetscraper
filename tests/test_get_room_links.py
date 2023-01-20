import unittest
from scraper import get_room_links

class TestGetRoomLinks(unittest.TestCase):
    def test_get_room_links(self):
        # Test a valid link
        links = get_room_links("https://kamernet.nl/huren/kamers-nederland")
        self.assertIsInstance(links, list)
        self.assertGreater(len(links), 0)
        self.assertTrue(all(map(lambda x: x.startswith("https://kamernet.nl"), links)))
        
        # Test an invalid link
        links = get_room_links("https://kamernet.nl/huren/kamers-nederland/invalid")
        self.assertEqual(links, [])

if __name__ == '__main__':
    unittest.main()
