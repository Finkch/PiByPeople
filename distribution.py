# Uses random distributions to determine just how bad
# the humans did at generating pi.

from random_numbers import random, initialise_random
from numpy import array, histogram, sqrt, pi, ndarray
import numpy as np
from calculate import is_coprime
from logger import logger
from typing import Callable
from scipy.optimize import curve_fit
from scipy.special import factorial
from sympy import divisors

# Generators


# Guess distributions
def inverse(x, a, b, c):
    return a / (x - c) + b

def simple_inverse(x, a):
    return a / x

def poisson(x, l, a):
    return a * ((l ** x) * (np.e ** -l)) / factorial(x)

def inverse_log(x, a, b, c):
    return a / np.log(x + b) + c




# Contains a distribution of data.
#   The function passed must return (y: float or similar) data given (x, *args).
class Distribution:
    def __init__(self, function: Callable, *args) -> None:
        self.function = function
        self.args = args

    
    # Generates the curve associated with this function
    def generate(self, num_range: range, *args) -> tuple:
        
        # Generate x data
        self.x = array([point for point in num_range])

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
        self.x, self.y = self.generator(self.trials, self.args)

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
            'dist':     Distribution(function, params),
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

        print(f'Slicing!:\t{start} : {stop}')

                
        # Trims and returns the arrays
        return x[start : stop], y[start : stop]

        
        