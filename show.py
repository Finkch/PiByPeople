# Shows the results

import matplotlib.pyplot as plt
from numpy import pi

from distribution import RandomDistribution
from dataset import Dataset



# Returns `π ± unc` with some formatting
def show_pi(guess_pi: float) -> str:

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
def print_pi(guess_pi: float) -> None:
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
def plot(dist: RandomDistribution, dataset: Dataset, num_range: list = None, is_log: bool = False, save: bool = False):

    # Gets the points for the random distribution
    points = (dist.x, dist.y)
        
    # Plots the random distribution data
    plot_scatter(points)
    plot_guesses(dist, num_range)

    # Finishing touches
    plt.legend()
    if is_log:
        plt.xscale('log')

    # Shows the graph
    if not save:
        plt.show()
    else:
        plt.savefig()


# Plots the distribution
def plot_scatter(points: tuple) -> None:
    plt.scatter(*points)

# Plots the theoretical distribution
def plot_guesses(dist: RandomDistribution, num_range: list = None) -> None:

    # Grabs the dictionary of distributions for easy reference
    dists = dist.dists

    # Gets the range for the guessed curve
    if not num_range:
        start, stop, steps = dist.x[0], dist.x[-1], 100
        num_range = [start + i / steps for i in range(int((stop - start) * steps))]

    # Plots each guess distribution
    for guess in dists:
        curve = dist.get_curve(guess, num_range)
        
        print(f'{guess}:')
        for i in range(len(dists[guess]['params'])):
            print(f'\t{dists[guess]["params"][i]} ± {dists[guess]["uncs"][i]}')

        plt.plot(*curve, label = guess)
