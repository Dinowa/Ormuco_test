import unittest
from compareVersion import compareVersion


class TestsForCompareVersion(unittest.TestCase):
    def test_Samelen_Smaller(self):
        v1, v2 = "1.2", "1.3"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is smaller than {v2}')

    def test_Samelen_Larger(self):
        v1, v2 = "1.3", "1.2"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is larger than {v2}')

    def test_Samelen_Same(self):
        v1, v2 = "1.2", "1.2"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is the same as {v2}')

    def test_Difflen_Same(self):
        v1, v2 = "1.0002", "1.02"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is the same as {v2}')

    def test_Difflen_Same2(self):
        v1, v2 = "1.2", "1.2.0"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is the same as {v2}')

    def test_Difflen_Larger(self):
        v1, v2 = "1.2.3", "1.02"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is larger than {v2}')

    def test_Difflen_Smaller(self):
        v1, v2 = "1.2.3", "1.2.3.6"
        result = compareVersion(v1, v2)
        self.assertEqual(result, f'{v1} is smaller than {v2}')


if __name__ == "__main__":
    unittest.main()