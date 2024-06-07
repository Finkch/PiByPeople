# Uses random distributions to determine just how bad
# the humans did at generating pi.

from random_numbers import random, initialise_random
from numpy import array, histogram, sqrt, pi, ndarray
import numpy as np
from calculate import is_coprime, cfs
from logger import logger
from typing import Callable
from scipy.optimize import curve_fit
from scipy.special import factorial
from sympy import divisors, gcd



# Contains a distribution of data.
#   The function passed must return (y: float or similar) data given (x, *args).
class Distribution:
    def __init__(self, function: Callable, *args) -> None:
        self.function = function
        self.args = args

    
    # Generates the curve associated with this function
    def generate(self, num_range: range, *args) -> tuple:
        
        # Gets the x values
        self.x = [x for x in num_range]

        # Ensures the first hundred values are extra dense.
        # This way, it looks smoother
        if len(self.x) > 100:
            self.x = [i / 10 for i in range(self.x[0] * 10, self.x[100] * 10)] + self.x[100:]

        # If no args were supplied, use the args sent during initialisation
        if not args:
            args = self.args

        # Generate y data
        self.y = array([self.function(point, *args) for point in self.x])

        return self.x, self.y



# Contains a distribution generated by random trials.
#   The generator must return both (x: ndarray, y: ndarray) given (trials, args).
class RandomDistribution:
    def __init__(self, generator: Callable, trials: int, *args) -> None:
        self.generator = generator
        self.trials = trials
        self.args = args

        self.dists  = {}

        self.generate()

    # Generates the random distribution
    def generate(self) -> tuple[ndarray, ndarray]:
        self.x, self.y = self.generator(self.trials, *self.args)

        return self.x, self.y

    # Obtains the theoretical curve of a guess distribution    
    def get_curve(self, name: str, num_range: range) -> tuple[ndarray, ndarray]:
        return self.dists[name]['dist'].generate(num_range)


    # Adds a guess of the underlying distribution
    def guess(self, function: Callable, name: str, guesses: tuple | None = None) -> None:
        
        # Tries to fit the guess to the random distribution
        params, cov = curve_fit(function, self.x, self.y, p0 = guesses)
        
        # Calculates the uncertainty of each variable
        uncs = np.sqrt(np.diag(cov))
        
        # Adds the Distribution
        self.dists[name] = {
            'dist':     Distribution(function, *params),
            'params':   params,
            'cov':      cov,
            'uncs':     uncs
        }


    
# Runs much faster than regular distribution, but less useful.
#   Used for generating histogram.
class SmallDistribution:
    def __init__(self, trials: int, length: int, max_num = 1e5) -> None:
        self.trials = trials
        self.length = length

        self.distribution = self.generate()

    # Generates a bunch of distributions
    def generate(self):

        # Sets the seed using system time
        initialise_random(None)

        dist = []
        for i in range(self.trials):
            
            # Gets the data for a single distribution.
            # We only care about the coprimes, for performance reasons
            coprimes = sum([
                is_coprime(
                    [random(end=1e5), random(end=1e5)] # Pairs of random numbers!
                ) for j in range(self.length)
            ])

            dist.append(coprimes)


        # Calculates π
        pis = sqrt(6 / array(dist) * self.length)

        return pis
    
    # Creates a numpy histogram of the distribution data
    def histogram(self, bin_size: float = None) -> tuple[ndarray, ndarray, float]:

        if not bin_size:
            bin_size = 1 / sqrt(self.length)


        # Gets a bunch of reasonably sized bins
        bins = [pi + bin_size * (i - 0.5) for i in range(-30, 30)]

        y, x = histogram(self.distribution, bins)

        logger.log('dist print', [str(datum) for datum in x] + ['\n\n'] + [str(datum) for datum in y])

        # Grabs the histogram, trimming of excess zeroes
        x, y = self.trim_histogram(y, x)

        x += bin_size / 2

        return x, y, bin_size


    # Removes excess zereos.
    #   NOTE: the order is (y, x), the return order for np.histogram()
    def trim_histogram(self, y: ndarray, x: ndarray) -> tuple[ndarray]:
        
        # Finds the last leading zero
        start = 0
        for i in range(len(y)):
            if y[i] != 0:
                start = i
                break
        
        # Finds the first trailing zero
        stop = 0
        for i in range(len(y) - 1, 0, -1):
            if y[i] != 0:
                stop = i + 1
                break

                
        # Trims and returns the arrays
        return x[start : stop], y[start : stop]

        
        






# Generators

# Generic generator returns a histogram, given a specific generator.
#   The specific generator must return a list
def generic_generator(nums: int, max_num: int, specific_generator: Callable, specific_counter: Callable, *args) -> tuple[ndarray, ndarray]:
    initialise_random(None)

    # Generates the requisite amount of random numbers
    counts = {}
    for i in range(nums):

        # Generates items
        gen = specific_generator(max_num, *args)

        # Counts the generated items
        specific_counter(gen, counts)
        
    
    # Sorts the dictionry to be in ascending order of x (aka key)
    counts = dict(sorted(counts.items()))

    for key in counts:
        logger.loga('cfs', f'{key}:\t{counts[key]}')
    
    # Return a list of the number versus its count
    return array(list(counts.keys())), array(list(counts.values()))

# Counts items in generated like a histogram
def generic_counter(generated: list | dict, counts: dict) -> None:
    for num in generated:
        if num not in counts:
            counts[num] = 0
        counts[num] += 1

# The distribution that is the factors of n
def factors(nums: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = nums,
        max_num = max_num, 
        specific_generator = lambda max_nums: 
            divisors(random(end = max_nums)),
        specific_counter = generic_counter
    )

# The distribution that is the common factors of n and m
def common_factors(pairs: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = pairs,
        max_num = max_num, 
        specific_generator = lambda max_num: 
            cfs(random(end = max_num), random(end = max_num)),
        specific_counter = generic_counter
    )

# The distribution that is the greatest common denominator of n and m
def greatest_common_denominator(pairs: int, max_num: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        nums = pairs,
        max_num = max_num,
        specific_generator = lambda max_num:
            [gcd(random(end = max_num), random(end = max_num))],
        specific_counter = generic_counter
    )

# Gets the count of gcd's that equal n
def gcd_is_n(pairs: int, max_num: int, n: int) -> tuple[ndarray, ndarray]:
    return generic_generator(
        pairs,
        max_num,
        gcd_specific,
        generic_counter,
        n
    )

# This is too complicated to fit into a lambda, to here's
# the specific generator for gcd_is_n
def gcd_specific(max_num: int, n: int) -> dict[int]:
    a, b = random(end = max_num), random(end = max_num)
    d = gcd(a, b)
    return {d: 1} if d == n else {}


# Distribution generators.
#   In other words, distributions of distributions.

# Returns a generator to create gcd_is_n distributions
def dist_gcd_is_n(trials: int, max_num: int, length, n: int) -> tuple[ndarray, tuple]:
    return generic_generator(
        trials,
        max_num,
        dist_gcd_spcific,
        generic_counter,
        length,
        n
    )

def dist_gcd_spcific(max_num: int, length: int, n: int) -> list:
    return [sum([
        is_coprime(
            [random(end = max_num), random(end = max_num)]
        ) for j in range(length)
    ])]


# Returns a generator to create gcd_is_n RandomDistributions
def dist_dist_gcd_is_n(trials: int, max_num: int, length: int, n: int) -> tuple[ndarray, tuple]:
    return generic_generator(
        trials,
        max_num,
        lambda max_num, length, n:
            RandomDistribution(gcd_is_n, length, max_num, n).y,
        generic_counter,
        length,
        n
    )


# Guess distributions
def inverse(x, a, b, c):
    return a / (x - c) + b

def simple_inverse(x, a):
    return a / x

def poisson(x, l, a):
    return a * ((l ** x) * (np.e ** -l)) / factorial(x)

def inverse_log(x, a, b, c):
    return a / np.log(x + b) + c