"""
Unit tests for randtest
"""

import unittest
from types import GeneratorType
from randtest import randtest


class TestRandTest(unittest.TestCase):
    """Unittesting randtest()"""

    def test_randtest_systematic_twosided(self):
        """Simple functionality test: systematic, two_sided randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_greater(self):
        """Simple functionality test: systematic, greater randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="greater",
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_less(self):
        """Simple functionality test: systematic, less randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="less",
        )
        self.assertEqual(1, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_twosided(self):
        """Multiproc. functionality test: systematic, two_sided randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="two_sided",
            num_jobs=-1,
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_greater(self):
        """Multiproc. functionality test: systematic, greater randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="greater",
            num_jobs=-1,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_less(self):
        """Multiproc. functionality test: systematic, less randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="less",
            num_jobs=-1,
        )
        self.assertEqual(1, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug(self):
        """Smart drug data: systematic, two_sided randtest()"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            num_permutations=30,
            alternative="two_sided",
            num_jobs=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)

    def test_randtest_systematic_twosided_mct_func(self):
        """Test supplying a function to mct"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            mct=mct_func_mean,
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_mct_func_mean(self):
        """Smart drug data: systematic, two_sided randtest(): mct mean func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            mct=mct_func_mean,
            num_permutations=1000,
            alternative="two_sided",
            num_jobs=-1,
            seed=0,
        )
        self.assertEqual(128, test_result.num_successes)
        self.assertEqual(1000, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_mct_func_tmean(self):
        """Smart drug data: systematic, two_sided randtest(): mct tmean func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            mct=mct_func_trimmed_mean,
            num_permutations=1000,
            alternative="two_sided",
            num_jobs=-1,
            seed=0,
        )
        self.assertEqual(10, test_result.num_successes)
        self.assertEqual(1000, test_result.num_permutations)

    def test_randtest_systematic_twosided_tstat_func(self):
        """Test supplying a function to test statistic"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            tstat=test_statistic_difference,
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_tstat_func(self):
        """Smart drug data: systematic, two_sided randtest(): tstat func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            tstat=test_statistic_difference,
            num_permutations=30,
            alternative="two_sided",
            num_jobs=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)


def mct_func_mean(data: GeneratorType) -> float:
    """MCT test function: mean"""
    # You are starting the pool before you define your function and classes,
    # that way the child processes cannot inherit any code. Move your pool
    # start up to the bottom and protect it with if __name__ == '__main__':
    # Then a lambda should work as well.
    #
    # HERE: define mct_func_mean function to be used
    sum_data_pnts, num_data_pnts = 0, 0
    for item in data:
        sum_data_pnts += item
        num_data_pnts += 1
    return sum_data_pnts / num_data_pnts


def mct_func_trimmed_mean(data: GeneratorType, trim_percent=.2) -> float:
    """MCT test function: trimmed mean"""
    data_sorted = tuple(sorted(data))
    num_data_pnts = len(data_sorted)
    lowercut = int(num_data_pnts * trim_percent)
    uppercut = num_data_pnts - lowercut
    data_trimmed = data_sorted[lowercut:uppercut]
    return sum(data_trimmed) / len(data_trimmed)


def test_statistic_difference(data1, data2, mct) -> float:
    """Test function for test statistic: Difference between MCT"""
    return mct(data1) - mct(data2)


if __name__ == "__main__":
    unittest.main()
