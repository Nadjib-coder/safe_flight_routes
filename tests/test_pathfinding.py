import unittest
from src.pathfinding import find_safe_path

class TestPathfinding(unittest.TestCase):
    
    def setUp(self):
        self.start = (0, 0)
        self.goal = (5, 5)
        self.wildfire_data = {
            "features": [
                {"geometry": {"coordinates": [[[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]]}}
            ]
        }
        self.volcanic_ash_data = {
            "features": [
                {"geometry": {"coordinates": [[[3, 3], [3, 4], [4, 4], [4, 3], [3, 3]]]}}
            ]
        }

    def test_find_safe_path(self):
        path = find_safe_path(self.start, self.goal, self.wildfire_data, self.volcanic_ash_data)
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 0)

if __name__ == '__main__':
    unittest.main()
