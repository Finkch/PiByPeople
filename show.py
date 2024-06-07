# Shows the results

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from statistics import stdev

from distribution import RandomDistribution

from logger import logger


# Returns `π ± unc` with some formatting
def show_pi(guess_pi) -> str:

    # Finds the absolute error
    absolute_error = abs(pi - guess_pi)

    # The relative error
    relative_error = absolute_error / pi * 100

    # The pricision at which to round
    precision = find_rounding(absolute_error)

    # Formats
    abs_pi = f'{guess_pi:.{precision}f} ± {absolute_error:.{precision}f}'
    rel_pi = f'{guess_pi:.{precision}f} ({relative_error:.{precision - 2}f}%)'

    return abs_pi, rel_pi

# Prints out the strings
def print_pi(guess_pi) -> None:
    abs_pi, rel_pi = show_pi(guess_pi)
    print(f'{abs_pi}\t\t{rel_pi}')


# Find the pricision at which to round.
#   This shows one more digit than it should for
#   showing uncertainty, but there is no fund to
#   be found is showing such truncated numbers.
def find_rounding(error: float) -> int:
    i = 0
    while error <= 1:
        error *= 10
        i += 1

    return i + 1



# Plots a random distribution and the guesses underlying it
def plot(dist: RandomDistribution):

    # Gets the points for the random distribution
    points = (dist.x, dist.y)
    num_range = range(int(points[0][0]), int(points[0][-1]))

    # Plots each guess distribution
    for guess in dist.dists:
        curve = dist.get_curve(guess, num_range)
        plt.plot(*curve, label = guess)

    # Displays
    plt.scatter(*points)
    plt.xscale('log')
    plt.legend()
    plt.show()


# A normal distribution
def normal(x: float, mean: float, sd: float) -> list[float]:
    prefactor = 1 / sd / np.sqrt(2 * pi)
    
    return prefactor * np.e ** (-0.5 * ((x - mean) / sd) ** 2)

# Returns a pair of lists that represent a normal distribution
def produce_normal(mean: float, sd: float, step_size: float = 0.01):
    x = np.arange(pi - 2 * sd, pi + 2 * sd, step_size)
    y = normal(x, mean, sd)

    return x, y

def get_sd(x: list, mean: float):
    return stdev(x, mean)




    
