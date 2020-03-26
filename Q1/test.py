import unittest
from Q1.Overlap import overlap


class TestsForOverLap(unittest.TestCase):
    def test_PositiveInt_OverLap(self):
        result = overlap([1, 5], [3, 6])
        self.assertEqual(result, True)

    def test_PositiveInt_NotOverLap(self):
        result = overlap([1, 5], [6, 12])
        self.assertEqual(result, False)

    def test_NegativeInt_OverLap(self):
        result = overlap([-1, -5], [-3, -6])
        self.assertEqual(result, True)

    def test_NegativeInt_NotOverLap(self):
        result = overlap((-1, -5), (-6, -11))
        self.assertEqual(result, False)

    def test_Integers_OverLap(self):
        result = overlap((-1, 2), (0, -2))
        self.assertEqual(result, True)

    def test_Origin_OverLap(self):
        result = overlap((0, 0), (0, 0))
        self.assertEqual(result, True)

    def test_Neighbour_OverLap(self):
        result = overlap((0, 2), (2, 3))
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()