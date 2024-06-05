# Shows the results

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

from distribution import Distribution


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


def plot_distribution(distribution: Distribution):

    # Produces a histogram from the random trials
    y, x = distribution.histogram()
    x = x[:len(y)]
    y = y / distribution.trials
    bins = plt.bar(x, y, 0.09)

    # Compares to a perfect normal distribution
    plt.plot(*produce_normal(pi, 1))

    plt.show()


# A normal distribution
def normal(x: float, mean: float, std: float) -> list[float]:
    prefactor = 1 / std / np.sqrt(2 * pi)
    
    return prefactor * np.e ** (-0.5 * ((x - mean) / std) ** 2)

# Returns a pair of lists that represent a normal distribution
def produce_normal(mean: float, std: float):
    x = np.arange(pi - 2 * std, pi + 2 * std, 0.01)
    y = normal(x, mean, std)

    return x, y



    
