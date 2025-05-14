import unittest
from shapely.geometry import Point
from src.geospatial import is_in_dangerous_area

class TestGeospatial(unittest.TestCase):
    
    def setUp(self):
        self.point_safe = (0, 0)
        self.point_danger = (1, 1)
        self.wildfire_data = {
            "features": [
                {"geometry": {"coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}}
            ]
        }
        self.volcanic_ash_data = {
            "features": [
                {"geometry": {"coordinates": [[[2, 2], [2, 3], [3, 3], [3, 2], [2, 2]]]}}
            ]
        }

    def test_is_in_dangerous_area_safe(self):
        result = is_in_dangerous_area(self.point_safe, self.wildfire_data, self.volcanic_ash_data)
        self.assertFalse(result)

    def test_is_in_dangerous_area_danger(self):
        result = is_in_dangerous_area(self.point_danger, self.wildfire_data, self.volcanic_ash_data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
