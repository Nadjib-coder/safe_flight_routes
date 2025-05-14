import unittest
from src.data_fetcher import fetch_airplane_data, fetch_wildfire_data, fetch_volcanic_ash_data

class TestDataFetcher(unittest.TestCase):
    
    def test_fetch_airplane_data(self):
        data = fetch_airplane_data()
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)

    def test_fetch_wildfire_data(self):
        data = fetch_wildfire_data()
        self.assertIn('features', data)
        self.assertIsInstance(data['features'], list)

    def test_fetch_volcanic_ash_data(self):
        data = fetch_volcanic_ash_data()
        self.assertIn('features', data)
        self.assertIsInstance(data['features'], list)

if __name__ == '__main__':
    unittest.main()
