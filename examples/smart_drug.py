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

import pathlib
from statistics import mean
from types import GeneratorType
from randtest import randtest


def smart_drug(mct, nperm=1000, seed=0):
    """Randomization test with smart drug data"""
    # First parent refers to the directory of the script
    parent_directory = str(pathlib.Path(__file__).parent.parent.resolve())
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
        num_jobs=-1,
        seed=seed)
    print(result)


def trimmed_mean(data: GeneratorType, trim_percent=.2) -> float:
    """Trimmed mean"""
    data_sorted = tuple(sorted(data))
    num_data_pnts = len(data_sorted)
    lowercut = int(num_data_pnts * trim_percent)
    uppercut = num_data_pnts - lowercut
    data_trimmed = data_sorted[lowercut:uppercut]
    return sum(data_trimmed) / len(data_trimmed)


def main():
    """Main function"""
    print(__doc__)
    print("MCT = Arithmetic Mean")
    smart_drug(mean)
    print()

    print("MCT = 20% Trimmed Mean")
    smart_drug(trimmed_mean)


if __name__ == '__main__':
    main()
