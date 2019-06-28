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
            num_cores=-1,
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
            num_cores=-1,
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
            num_cores=-1,
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
            num_cores=-1,
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

    def test_randtest_monte_multiproc_twosided_smartdrug_mct_func(self):
        """Smart drug data: systematic, two_sided randtest(): mct func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            mct=mct_func_mean,
            num_permutations=30,
            alternative="two_sided",
            num_cores=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)

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
            num_cores=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)


def mct_func_mean(data_generator):
    """MCT test function: mean"""
    # You are starting the pool before you define your function and classes,
    # that way the child processes cannot inherit any code. Move your pool
    # start up to the bottom and protect it with if __name__ == '__main__':
    # Then a lambda should work as well.
    #
    # HERE: define mct_func_mean function to be used
    data_sum, data_len = 0, 0
    for item in data_generator:
        data_sum += item
        data_len += 1
    return data_sum / data_len


def test_statistic_difference(data1, data2, mct):
    """Test function for test statistic: Difference between MCT"""
    return mct(data1) - mct(data2)


if __name__ == "__main__":
    unittest.main()
