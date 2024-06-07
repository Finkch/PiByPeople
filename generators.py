# Generators to generate sets of numbers for distributions

from random_numbers import random, initialise_random
from numpy import array, ndarray
from calculate import cfs
from typing import Callable
from sympy import divisors, gcd
from distribution import RandomDistribution, PiDistribution


# Generic generator returns a histogram, given a specific generator.
#   The specific generator must return a list
def generic_generator(nums: int, max_num: int, specific_generator: Callable, *args) -> tuple[ndarray, ndarray]:
    initialise_random(None)

    # Generates the requisite amount of random numbers
    counts = {}
    for i in range(nums):

        # Generates items
        generated = specific_generator(max_num, *args)

        # Counts the generated items
        for num in generated:
            if num not in counts:
                counts[num] = 0
            counts[num] += 1
        
    
    # Sorts the dictionry to be in ascending order of x (aka key)
    counts = dict(sorted(counts.items()))
    
    # Return a list of the number versus its count
    return array(list(counts.keys())), array(list(counts.values()))



#   Specific generators

# The distribution that is the factors of n
def factors(nums: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = nums,
        max_num = max_num, 
        specific_generator = lambda max_nums: 
            divisors(random(end = max_nums)),
    )

# The distribution that is the common factors of n and m
def common_factors(pairs: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = pairs,
        max_num = max_num, 
        specific_generator = lambda max_num: 
            cfs(random(end = max_num), random(end = max_num)),
    )

# The distribution that is the greatest common denominator of n and m
def greatest_common_denominator(pairs: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = pairs,
        max_num = max_num,
        specific_generator = lambda max_num:
            [gcd(random(end = max_num), random(end = max_num))],
    )

# Gets the count of gcd's that equal n
def gcd_is_n(pairs: int, max_num: int, n: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        pairs,
        max_num,
        gcd_specific,
        n
    )

# Gets the count of gcd's that equal to 1, e.i. they are coprime
def coprime(pairs: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        pairs,
        max_num,
        lambda max_num: 
            {1: 1} if gcd(random(end = max_num), random(end = max_num)) == 1 else {}
    )

# This is too complicated to fit into a lambda, to here's
# the specific generator for gcd_is_n
def gcd_specific(max_num: int, n: int) -> dict[int]:
    a, b = random(end = max_num), random(end = max_num)
    d = gcd(a, b)
    return {d: 1} if d == n else {}



#   Distribution generators.
#   In other words, distributions of distributions.

# Returns a generator to create gcd_is_n RandomDistributions
def dist_dist_gcd_is_n(trials: int, max_num: int, length: int, n: int) -> tuple[ndarray, tuple]:
    return generic_generator(
        trials,
        max_num,
        lambda max_num, length, n:
            RandomDistribution(gcd_is_n, length, max_num, n).y,
        length,
        n
    )

def dist_pi(trials: int, max_num: int, length: int) -> tuple[ndarray, tuple]:
    return generic_generator(
        trials,
        max_num,
        lambda max_num, length:
            [PiDistribution(coprime, length, max_num).pi],
        length
    )