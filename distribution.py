# Uses random distributions to determine just how bad
# the humans did at generating pi.

from numpy import array, sqrt, ndarray
import numpy as np
from typing import Callable
from scipy.optimize import curve_fit
from scipy.stats import percentileofscore
from calculate import normalisation_factor



# Contains a distribution of data.
#   The function passed must return (y: float or similar) data given (x, *args).
class Distribution:
    def __init__(self, function: Callable, *args) -> None:
        self.function = function
        self.args = args

    
    # Generates the curve associated with this function
    def generate(self, num_range: list, *args) -> tuple:
        
        # Grabs the x values
        self.x = num_range

        # Ensures the first ten values are extra dense.
        # This way, it looks smoother
        if len(self.x) > 10:
            self.x = [i / 10 for i in range(int(self.x[0] * 10), int(self.x[10] * 10))] + self.x[10:]

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
    def guess(self, function: Callable, name: str, guesses: tuple) -> None:
        
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

    # Normalises the y-values
    def normalise(self, height: float = None):

        # Sets the max height to one
        self.y = np.divide(self.y, max(self.y))

        # If height is specified, set the max height to it
        if height:
            self.y = np.multiply(self.y, height)

        # Otherwise, normalise
        else:
            self.y = np.multiply(self.y, normalisation_factor(self.x, self.y))

    # Finds the percentile in which a value lies.
    #   NOTE: this method only correctly if the (x, y) data
    #   takes the form of a histogram. That is, the y data
    #   consists of positive integers.
    #
    #   NOTE: This assumes the random distribution has
    #   converged to the true distribution.
    def percentile(self, value: float) -> float:
        
        # Adds "weights"
        vals = []
        for i in range(len(self.x)):
            vals += [self.x[i] for j in range(self.y[i])]

        # Returns the percentile
        return percentileofscore(vals, value, kind = 'mean')
    
    # Find how close to the top a value lies in the percentile
    #   NOTE: This assumes the random distribution has
    #   converged to the true distribution.
    def top_percent(self, value: float):
        return abs(self.percentile(value) - 50) * 2
        
    # Finds how close to the bottom relative to the mean a value is
    #   NOTE: Unlike top_percent() and percentile(), this does not
    #   assume the distribution has converged to the true distribution.
    def bottom_percent(self, value: float, mean: float) -> float:
        
        # Gets the error of the value in question
        value_error = abs(mean - value)

        # Gets a sorted list of the absolute errors from the mean
        errors = {abs(mean - self.x[i]): self.y[i] for i in range(len(self.x))}
        errors = dict(sorted(errors.items(), reverse = True))

        # Computes the score of the item
        score = 0

        # Iterates over all the items
        for error in errors:

            # Finds the position within the error
            if value_error > error:
                break

            # Adds the weight in this bin of error
            score += errors[error]

        # Scales to [0, 100]
        return 100 * score / self.trials

    # Returns a list representing the range of numbers
    def range(self, steps: int = 1000) -> list[float]:
        
        # Gets the minimum and maximum x values, and the span between them
        mini, maxi = min(self.x), max(self.x)
        diff = maxi - mini

        # Gives the range a bit of wiggle room
        left = mini - diff / 8
        if mini == 1:   # Some distributions don't like less than 1
            left = mini

        right = maxi + diff / 8
        diff = right - left

        # Calculates the step size needed to span the range
        size = diff / steps

        # Creates the range of numbers
        return [left + step * size for step in range(steps)]



# A random distribution specifically for calculating pi.
#   `generator` should be coprime, but that can't be enforce
#   due to circular imports.
class PiDistribution(RandomDistribution):
    def __init__(self, generator: Callable, trials: int, *args) -> None:
        
        # We want a coprime distribution to transform into a guess for π 
        super().__init__(generator, trials, *args)

    # Generates a random distribution to guess at π
    def generate(self) -> tuple[ndarray, ndarray]:
        super().generate()

        # Sets trials in case the trials is not known beforehand.
        # Used when the generator reads from a file.
        if self.trials == None:
            self.trials = self.x[0]

        # Calculates π
        self.pi = sqrt(6 / (self.y[0] / self.trials))

