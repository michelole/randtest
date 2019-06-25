"""
Unit tests for randtest
"""

import unittest
from randtest import randtest


class TestRandTest(unittest.TestCase):
    """Unittesting randtest()"""

    def test_randtest_systematic_twosided(self):
        """Simple functionality test: systematic, two_sided randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            method="systematic",
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_hits)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_greater(self):
        """Simple functionality test: systematic, greater randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            method="systematic",
            alternative="greater",
        )
        self.assertEqual(6, test_result.num_hits)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_less(self):
        """Simple functionality test: systematic, less randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            method="systematic",
            alternative="less",
        )
        self.assertEqual(1, test_result.num_hits)
        self.assertEqual(6, test_result.num_permutations)


if __name__ == "__main__":
    unittest.main()
