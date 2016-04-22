#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from randomization_tests import RandomizationTests

groupA_data = [5, 6]
groupB_data = [8, 10]

sys_rtest = RandomizationTests(method='systematic')
sys_rtest.execute(groupA_data, groupB_data)


class TestSystematicRandomizationTests(unittest.TestCase):

    def test_groupA_mean(self):
        self.assertEqual(sys_rtest._mctA, 5.5)

    def test_groupB_mean(self):
        self.assertEqual(sys_rtest._mctB, 9.0)

    def test_tobs(self):
        self.assertEqual(sys_rtest._tobs, -3.5)

    def test_count(self):
        self.assertEqual(sys_rtest._count, 2)

    def test_nperm(self):
        self.assertEqual(sys_rtest._nperm, 6)

    def test_pvalue(self):
        self.assertEqual(sys_rtest.pvalue, 2 / 6)


sys_rtest_greater = RandomizationTests(
    method='systematic',
    alternative='greater',
)
sys_rtest_greater.execute(groupA_data, groupB_data)


class TestSystematicRandomizationTestsGreater(unittest.TestCase):

    def test_groupA_mean(self):
        self.assertEqual(sys_rtest_greater._mctA, 5.5)

    def test_groupB_mean(self):
        self.assertEqual(sys_rtest_greater._mctB, 9.0)

    def test_tobs(self):
        self.assertEqual(sys_rtest_greater._tobs, -3.5)

    def test_count(self):
        self.assertEqual(sys_rtest_greater._count, 6)

    def test_nperm(self):
        self.assertEqual(sys_rtest_greater._nperm, 6)

    def test_pvalue(self):
        self.assertEqual(sys_rtest_greater.pvalue, 6 / 6)

sys_rtest_less = RandomizationTests(method='systematic', alternative='less')
sys_rtest_less.execute(groupA_data, groupB_data)


class TestSystematicRandomizationTestsLess(unittest.TestCase):

    def test_groupA_mean(self):
        self.assertEqual(sys_rtest_less._mctA, 5.5)

    def test_groupB_mean(self):
        self.assertEqual(sys_rtest_less._mctB, 9.0)

    def test_tobs(self):
        self.assertEqual(sys_rtest_less._tobs, -3.5)

    def test_count(self):
        self.assertEqual(sys_rtest_less._count, 1)

    def test_nperm(self):
        self.assertEqual(sys_rtest_less._nperm, 6)

    def test_pvalue(self):
        self.assertEqual(sys_rtest_less.pvalue, 1 / 6)


mc_rtest = RandomizationTests(method='monte', seed=42)
mc_rtest.execute(groupA_data, groupB_data, 100)


class TestMonteCarloRandomizationTests(unittest.TestCase):

    def test_groupA_mean(self):
        self.assertEqual(mc_rtest._mctA, 5.5)

    def test_groupB_mean(self):
        self.assertEqual(mc_rtest._mctB, 9.0)

    def test_tobs(self):
        self.assertEqual(mc_rtest._tobs, -3.5)

    def test_count(self):
        self.assertEqual(mc_rtest._count, 37)

    def test_nperm(self):
        self.assertEqual(mc_rtest._nperm, 100)

    def test_pvalue(self):
        self.assertEqual(mc_rtest.pvalue, 37 / 100)

if __name__ == "__main__":
    unittest.main()
