import sys
import os
import unittest
from math import sqrt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
from lib.hard_coded import (
    filter_duplicate_colors
)
from lib.color_check import (are_colors_similar,
    is_color_in_samples)


class TestColorFunctions(unittest.TestCase):
    
    def test_filter_duplicate_colors(self):
        colors = [
            (193, 141, 132),
            (80, 91, 13),
            (129, 104, 64),
            (193, 141, 132),  # Duplicate
            (83, 95, 13)
        ]
        expected_unique_colors = [
            (193, 141, 132),
            (80, 91, 13),
            (129, 104, 64),
            (83, 95, 13)
        ]
        unique_colors = filter_duplicate_colors(colors)
        self.assertEqual(sorted(unique_colors), sorted(expected_unique_colors))

    def test_are_colors_similar(self):
        color1 = (100, 150, 200)
        color2 = (105, 155, 205)
        color3 = (200, 200, 200)
        tolerance = 10

        self.assertTrue(are_colors_similar(color1, color2, tolerance))
        self.assertFalse(are_colors_similar(color1, color3, tolerance))

    def test_is_color_in_samples(self):
        samples = [
            (193, 141, 132),
            (80, 91, 13),
            (129, 104, 64)
        ]
        color1 = (193, 141, 132)
        color2 = (83, 95, 13)  # This color is within tolerance of (80, 91, 13)
        color3 = (0, 0, 0)
        tolerance = 10  # Increase tolerance if necessary

        self.assertEqual(is_color_in_samples(color1, samples, tolerance), (193, 141, 132))
        self.assertEqual(is_color_in_samples(color2, samples, tolerance), (80, 91, 13))  # Expecting a match with tolerance
        self.assertEqual(is_color_in_samples(color3, samples, tolerance), None)

# if __name__ == '__main__':
#     unittest.main()