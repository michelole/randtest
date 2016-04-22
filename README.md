# Randomization tests for two-sample comparison
This Python package implements a randomization test for the comparison of two
independent groups as described in:
> E. Edgington and P. Onghena, Randomization Tests, 4th ed.<br/>
> Boca Raton, FL: Chapman & Hall/CRC, Taylor & Francis Group, 2007.

## Requirements

* Tested with Python 3 (not Python 2.7)

## Install

## Basic example

This example is taken from:
> E. Stripling, "Distribution-free statistical inference for the comparison of
> central tendencies," <br/> 
> MSc thesis, Dept. LStat, KU Leuven, Leuven, Belgium, 2013.

In a randomization test, the hypotheses are as follows:
<p align="center">
    <img src="misc/hypotheses.png" width="700"/>
</p>

Now, suppose we have two treatment groups, __A__ and __B__, and four
experimental units (designated as _a_, _b_, _c_, and _d_), which are randomly
assigned to the two treatment groups. We conduct the experiment and measure the
 response of the experimental units. Assume we observed the following data
<p align="center">
    <img src="misc/observed_data.png" width="400"/>
</p>

Our test statistic of interest is the difference between arithmetic means,
where _t<sub>obs</sub>_ is the observed test statistic value. Then, permute
the data and compute the test statistic for each data permutation, which
creates the _reference distribution_. In this example, the _systematic_
approach is used, meaning that all possible data permutations are generated.

<p align="center">
    <img src="misc/permutations.png" width="700"/>
</p>

Based on the data permutations, the two-sided p value can be computed:

<p align="center">
    <img src="misc/pvalue.png" width="450"/>
</p>

That is, simply count how often _T_ (in absolute sense) is equal to or
larger than |_t<sub>obs</sub>_|, and divide it by the number of data
permutations. In this example, the exact two-sided p value equals 2/6 or 33%.

To carry out the analysis in Python, do the following:

```python
>>> from randomization_tests import RandomizationTests
>>> groupA_data = [5, 6]
>>> groupB_data = [8, 10]
>>> sys_rtest = RandomizationTests(method='systematic')
>>> sys_rtest.execute(groupA_data, groupB_data)
>>> sys_rtest.summary()
Systematic randomization test for two groups
Alternative hypothesis: two_sided
Arithmetic mean of group A: 5.50
Arithmetic mean of group B: 9.00
Observed test statistic value: -3.50
Count: 2
Number of permutations: 6
p value: 0.3333
```

The systematic approach, however, quickly becomes infeasible if the sample size
increases. In this circumstances, the _Monte Carlo randomization test_ can be
used to approximate the p value, which is carried out by default:
`method='monte'`.

```python
>>> monte_rtest = RandomizationTests(seed=101)
>>> monte_rtest.execute(groupA_data, groupB_data, number_of_permutations=10000)
>>> monte_rtest.summary()
Monte Carlo randomization test for two groups
Alternative hypothesis: two_sided
Arithmetic mean of group A: 5.50
Arithmetic mean of group B: 9.00
Observed test statistic value: -3.50
Count: 3388
Number of permutations: 10000
p value: 0.3388
```


## Smart drug example
To illustrate randomization tests on a more realistic example, consider the
"smart drug" example described in
> J. K. Kruschke, "Bayesian estimation supersedes the t test."
> *Journal of Experimental Psychology: General*, <br/>
> vol. 142, no. 2, pp. 573-603, May 2013. [[Online](http://dx.doi.org/10.1037/a0029146)]

In which, the research question is: _Do people who take the smart drug perform_
_better on the IQ test than those in the control group?_
In the experiment, 47 people received the supposedly IQ-enhancement drug
(group A), and 42 people received an placebo (group B).
Data have been obtained from
[here](https://github.com/strawlab/best/blob/master/examples/smart_drug.py).

For this example, two randomization test are carried out: (1) one in which the
test statistic is the difference between arithmetic means, and (2) in which the
test statistic is the difference between trimmed means (20% on each side) in
order to account for the outliers in the data.


```bash
$ python examples/smart_drug.py
==================================================
Monte Carlo randomization test for two groups
Alternative hypothesis: two_sided
Arithmetic mean of group A: 101.91
Arithmetic mean of group B: 100.36
Observed test statistic value: 1.56
Count: 1252
Number of permutations: 10000
p value: 0.1252
- - - - - - - - - - - - - - - - - - - - - - - - -
Monte Carlo randomization test for two groups
Alternative hypothesis: two_sided
Trimmed Mean of group A: 101.59
Trimmed Mean of group B: 100.54
Observed test statistic value: 1.05
Count: 100
Number of permutations: 10000
p value: 0.0100
==================================================
```

For (1), the p value equals 12.52%, meaning that one does not reject the null
hypothesis at a significance level of 5%. However, this test is naive, since
the outliers cause a distortion of the arithmetic means. In (2), the test
statistic is robuster against extreme observations, resulting in p value of 1%.
Thus, with the more reasonable test statistic, the null hypothesis is rejected.
One can therefore conclude that the response of at least one person would have
been different if (s)he had received the other treatment. Note that the
rejection of the null hypothesis is in line with the conclusion of the robust
Bayesian estimation approach carried out by Kruschke.
