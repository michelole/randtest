# Randomization tests for two-sample comparison
This Python package implements a randomization test for the comparison of two
independent groups as described in:
> E. Edgington and P. Onghena, Randomization Tests, 4th ed.<br/>
> Boca Raton, FL: Chapman & Hall/CRC, Taylor & Francis Group, 2007.


## Requirements

* Python 3


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
where _t<sub>obs</sub>_ is the observed test statistic value. 
For carry out the randomization test, permute the data and compute the test 
statistic for each data permutation, which creates the _reference distribution_.
In this example, the _systematic_ approach is used, meaning that all possible
data permutations are generated.

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

Use the `randtest` function to  carry out the analysis in Python.
Note that `num_permutations = -1` specifies the systematic approach.

```{python}
>>> from randtest import randtest
>>> x = (5, 6)
>>> y = (8, 10)
>>> result = randtest(x, y, num_permutations=-1)
>>> print(result)
<class 'randtest.base.RandTestResult'>
Method = Systematic
Alternative = two_sided
MCT(data of group A) = 5.5
MCT(data of group B) = 9
Observed test statistic value = -3.5
Number of successes = 2
Number of permutations = 6
p value = 0.333333
```

The systematic approach, however, quickly becomes infeasible if the sample size
increases. 
In this circumstances, the _Monte Carlo randomization test_ can be
used to approximate the p value. 
It is carried out by default with a positive number for `num_permutations`.

```{python}
>>> from randtest import randtest
>>> x = (5, 6)
>>> y = (8, 10)
>>> result = randtest(x, y, num_permutations=10000, num_cores=2, seed=0)
>>> print(result)
<class 'randtest.base.RandTestResult'>
Method = Monte Carlo
Alternative = two_sided
MCT(data of group A) = 5.5
MCT(data of group B) = 9
Observed test statistic value = -3.5
Number of successes = 3312
Number of permutations = 10000
p value = 0.3312
```


## Smart drug example
To illustrate randomization tests on a more realistic example, consider the
"smart drug" example described in [(Online)](http://dx.doi.org/10.1037/a0029146):
> J. K. Kruschke, "Bayesian estimation supersedes the t test."
> *Journal of Experimental Psychology: General*, <br/>
> vol. 142, no. 2, pp. 573-603, May 2013. 

In which, the research question is: _Do people who take the smart drug perform_
_better on the IQ test than those in the control group?_
In the experiment, 47 people received the supposedly IQ-enhancement drug
(group A), and 42 people received an placebo (group B).
Data have been taken from
[here](https://github.com/strawlab/best/blob/master/examples/smart_drug.py).

For this example, two randomization test are carried out: (1) one in which the
test statistic is the difference between arithmetic means, and (2) in which the
test statistic is the difference between trimmed means (20% on each side) in
order to account for the outliers in the data.


```{bash}
$ make example_smart_drug 
python3 examples/smart_drug.py
MCT = Arithmetic Mean
<class 'randtest.base.RandTestResult'>
Method = Monte Carlo
Alternative = two_sided
MCT(data of group A) = 101.915
MCT(data of group B) = 100.357
Observed test statistic value = 1.55775
Number of successes = 128
Number of permutations = 1000
p value = 0.128

MCT = 20% Trimmed Mean
<class 'randtest.base.RandTestResult'>
Method = Monte Carlo
Alternative = two_sided
MCT(data of group A) = 101.586
MCT(data of group B) = 100.538
Observed test statistic value = 1.04775
Number of successes = 10
Number of permutations = 1000
p value = 0.01
```

For (1), the p value equals 12.8%, meaning that one does not reject the null
hypothesis at a significance level of 5%. 
However, this test is naive, since the outliers cause a distortion of the 
arithmetic means. In (2), the test statistic is robuster against extreme 
observations, resulting in p value of 1%.
Thus, with the more reasonable test statistic, the null hypothesis is rejected.
One can therefore conclude that the response of at least one person would have
been different if (s)he had received the other treatment. 
Note that the rejection of the null hypothesis with (2) is in line with the 
conclusion of the robust Bayesian estimation approach carried out by Kruschke.
