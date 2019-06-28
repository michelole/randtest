"""
The data are taken from the example that reproduces Figure 3 of

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

from statistics import mean
from os.path import abspath, dirname, sep
from scipy import stats
from randtest import randtest


def smart_drug(mct, nperm=1000, seed=0):
    """Randomization test with smart drug data"""
    this_directory = dirname(__file__)
    parent_directory = abspath(
        '{}'.format(sep).join(this_directory.split(sep)[:-1])
    )
    ifname_group_a = (
        parent_directory + "/data/smart_drug_data_treatment_group.dat"
    )
    ifname_group_b = (
        parent_directory + "/data/smart_drug_data_placebo_group.dat"
    )
    with open(ifname_group_a, 'r') as fobj:
        group_a = tuple(int(val.strip()) for val in fobj.readlines())
    with open(ifname_group_b, 'r') as fobj:
        group_b = tuple(int(val.strip()) for val in fobj.readlines())

    result = randtest(
        group_a,
        group_b,
        mct,
        num_permutations=nperm,
        num_cores=-1,
        seed=seed)
    print(result)


def trimmed_mean(data, percent=0.2) -> float:
    """Trimmed mean"""
    mct_val = stats.trim_mean(tuple(data), percent)
    return float(mct_val)


def main():
    """Main function"""
    print("MCT = Arithmetic Mean")
    smart_drug(mean)
    print()

    print("MCT = 20% Trimmed Mean")
    smart_drug(trimmed_mean)


if __name__ == '__main__':
    main()
