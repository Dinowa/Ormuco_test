from Q3.DistributedCache import DistributedCache
import time
import unittest


class TestsForCache(unittest.TestCase):
    def test_capacity(self):
        cache = DistributedCache(4, 5)
        cache.put('a', '1')
        cache.put('b', '2')
        cache.put('c', '3')
        cache.put('d', '3')
        self.assertEqual(cache.get('b'), '2')
        cache.put('e', '4')
        self.assertEqual(cache.get('a'), None)
        cache.put('d', '5')
        self.assertEqual(cache.get('c'), '3')
        self.assertEqual(cache.get('d'), '5')
        cache.get('b')
        cache.put('f', '6')
        self.assertEqual(cache.get('e'), None)

    def test_timeExpire(self):
        cache = DistributedCache(4, 5)
        cache.put('a', '1')
        cache.put('b', '2')
        time.sleep(5)
        self.assertEqual(cache.get('a'), None)
        self.assertEqual(cache.get('b'), None)


if __name__ == "__main__":
    unittest.main()


