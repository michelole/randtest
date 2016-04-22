#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""The data are taken from the example that reproduces Figure 3 of

J. K. Kruschke, "Bayesian estimation supersedes the t test."
    Journal of Experimental Psychology: General,
    vol. 142, no. 2, pp. 573-603, May 2013.

According to the article, the data were generated from t distributions
of known values. Data are taken from:
https://github.com/strawlab/best/blob/master/examples/smart_drug.py

In this example, two randomization tests are performed to test whether
there is a significant difference between the two independent groups based on:

E. Edgington and P. Onghena, Randomization Tests, 4th ed.
    Boca Raton, FL: Chapman & Hall/CRC, Taylor & Francis Group, 2007.

In the first test, the test statistic is defined to be the difference between
arithmetic means. In the second test, the test statistic is defined to be the
difference between trimmed means (20% on each side) in order to account for
the outliers.
"""

from scipy import stats
from randomization_tests import RandomizationTests

SEED = 42  # To reproduce the results in the post
N_PERM = 10000  # Number of permutations

drug = (101, 100, 102, 104, 102, 97, 105, 105, 98, 101,
        100, 123, 105, 103, 100, 95, 102, 106, 109, 102,
        82, 102, 100, 102, 102, 101, 102, 102, 103, 103,
        97, 97, 103, 101, 97, 104, 96, 103, 124, 101,
        101, 100, 101, 101, 104, 100, 101)
placebo = (99, 101, 100, 101, 102, 100, 97, 101, 104, 101,
           102, 102, 100, 105, 88, 101, 100, 104, 100, 100,
           100, 101, 102, 103, 97, 101, 101, 100, 101, 99,
           101, 100, 100, 101, 100, 99, 101, 100, 102, 99,
           100, 99)


def trimmed_mean(x, percent=0.2):
    return stats.trim_mean(x, percent)

# Standard test statistic is the arithmetic mean
rtest_diff_means = RandomizationTests(seed=SEED)
rtest_diff_trimmed_means = RandomizationTests(
    trimmed_mean,
    'Trimmed Mean',
    seed=SEED,
    )

print('=' * 50)
rtest_diff_means.execute(drug, placebo, N_PERM)
rtest_diff_means.summary()
print('- ' * 25)
rtest_diff_trimmed_means.execute(drug, placebo, N_PERM)
rtest_diff_trimmed_means.summary()
print('=' * 50)
