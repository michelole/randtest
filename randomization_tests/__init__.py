#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Randomization tests for two-sample comparison

This module implements a randomization test for two independent groups.

Based on:

E. Edgington and P. Onghena, Randomization Tests, 4th ed.
    Boca Raton, FL: Chapman & Hall/CRC, Taylor & Francis Group, 2007.
"""

import types
from itertools import combinations
from numpy.random import RandomState


class RandomizationTests(object):
    """Randomization tests for two-sample comparison with user-defined test
    statistic
    """

    def __init__(
            self,
            measure_central_tendency=None,
            name='Arithmetic mean',
            method='monte',
            alternative='two_sided',
            seed=None):
        """Constructor"""
        self.mct = measure_central_tendency
        self.name = name
        self.method = method
        self.alternative = alternative
        self._1stexe = None  # first execution
        self._tobs = None  # observed test statistic value
        self._mctA = None
        self._mctB = None
        self._nA = None
        self._data = None
        self._indices = None
        self._count = 0
        self._nperm = 0  # Number of permutations
        self.pvalue = None
        self._prng = RandomState(seed)

    @property
    def mct(self):
        return self._mct

    @mct.setter
    def mct(self, value):
        if isinstance(value, types.FunctionType):
            self._mct = value
        else:
            self._mct = self._aritmetic_mean

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            if isinstance(value, str):
                self._name = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        assert value in ['systematic', 'monte']
        self._method = value

    @property
    def alternative(self):
        return self._alternative

    @alternative.setter
    def alternative(self, value):
        assert value in ['two_sided', 'greater', 'less']
        self._alternative = value

    def _compute_test_statistic(self, x, y):
        return self._mct(x) - self._mct(y)

    def _aritmetic_mean(self, x):
        return sum(x) / len(x)

    def _process_data_permutation(self, groupA_indices):
        self._nperm += 1
        groupB_indices = set(self._indices).difference(groupA_indices)
        t = self._compute_test_statistic(
            [self._data[i] for i in groupA_indices],
            [self._data[j] for j in groupB_indices],
            )
        if self._alternative == 'two_sided':
            self._count += 1 if abs(t) >= abs(self._tobs) else 0
        elif self._alternative == 'greater':
            self._count += 1 if t >= self._tobs else 0
        else:
            self._count += 1 if t <= self._tobs else 0

    def execute(self, x=None, y=None, number_of_permutations=10000):
        if x and y:
            if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
                if all([isinstance(i, (int, float)) for i in x]):
                    self._nA = len(x)
                    self._mctA = self._mct(x)
                else:
                    raise TypeError('Elements in x should be numbers')
                if all([isinstance(j, (int, float)) for j in y]):
                    self._mctB = self._mct(y)
                else:
                    raise TypeError('Elements in y should be numbers')
            self._1stexe = True
            self._tobs = self._compute_test_statistic(x, y)
            self._data = x + y
            self._indices = range(self._nA + len(y))
        assert isinstance(number_of_permutations, int)
        if self.method == 'monte':
            # Monte Carlo randomization test with valid p value, i.e.,
            # include t_obs to reference set
            if self._1stexe:
                self._1stexe = False
                self._count += 1
                self._nperm += 1
                number_of_permutations -= 1
            for _ in range(number_of_permutations):
                groupA_indices = self._prng.choice(
                    self._indices,
                    self._nA,
                    replace=False,
                    )
                self._process_data_permutation(groupA_indices)
        else:
            for groupA_indices in combinations(self._indices, self._nA):
                self._process_data_permutation(groupA_indices)
        self.pvalue = self._count / self._nperm

    def summary(self):
        if self.method == 'systematic':
            print('Systematic randomization test for two groups')
        else:
            print('Monte Carlo randomization test for two groups')
        print('Alternative hypothesis: {0}'.format(self._alternative))
        print('{0} of group A: {1:.2f}'.format(self._name, self._mctA))
        print('{0} of group B: {1:.2f}'.format(self._name, self._mctB))
        print('Observed test statistic value: {0:.2f}'.format(self._tobs))
        print('Count: {0:d}'.format(self._count))
        print('Number of permutations: {0:d}'.format(self._nperm))
        print('p value: {0:.4f}'.format(self.pvalue))
