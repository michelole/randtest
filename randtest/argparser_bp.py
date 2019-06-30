"""
argparse boilerplate code
"""

import ast
import argparse
import textwrap


def read_data(ifname):
    """Read in data: assuming no header, only numbers"""
    with open(ifname, 'r') as fobj:
        data = (
            ast.literal_eval(num.strip())
            for num in fobj.readlines()
        )
    return data


def argparse_cli(description):
    """argparse boilerplate code"""
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(description)
    )
    parser.add_argument(
        "-a",
        metavar="alternative",
        type=str,
        choices=["two_sided", "greater", "less"],
        default="two_sided",
        help="Alternative hypothesis (default: 'two_sided')."
    )
    parser.add_argument(
        "-p",
        metavar="num_permutations",
        type=int,
        default=10000,
        help="Number of permutations (default: 10000)."
    )
    parser.add_argument(
        "-n",
        metavar="num_jobs",
        type=int,
        default=1,
        help="Number of jobs (default: 1)."
    )
    parser.add_argument(
        "-s",
        metavar="seed",
        type=int,
        default=None,
        help="Seed to initialize the random number generator (default: None)",
    )

    parser.add_argument(
        "fname_data_A",
        type=str,
        help="File name group A data.",
    )
    parser.add_argument(
        "fname_data_B",
        type=str,
        help="File name group B data.",
    )
    return parser
