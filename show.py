# Shows the results

import matplotlib.pyplot as plt
from matplotlib.colors import TABLEAU_COLORS
from numpy import pi

from distribution import RandomDistribution
from dataset import Dataset

from logger import logger



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
def plot(dist: RandomDistribution, dataset: Dataset, num_range: list = None, title: str = None, axes: tuple[str] = None, is_log: bool = False, save: bool = False):

    # Gets the points for the random distribution
    points = (dist.x, dist.y)

    # Gets a list of colours to use
    colours = get_colours()
        
    # Plots the random distribution data
    plot_scatter(points, colours)
    plot_guesses(dist, colours, num_range = num_range)
    
    # Adds the dataset data
    plot_dataset(dataset, colours)

    # Finishing touches
    plot_titles(title, axes, is_log)
        

    # Shows the graph
    if not save:
        plt.show()
    else:
        plt.savefig()


# Plots the distribution
def plot_scatter(points: tuple, colours: list[str]) -> None:
    plt.scatter(*points, color = colours.pop(0), label = 'Random Distributions')

# Plots the theoretical distribution
def plot_guesses(dist: RandomDistribution, colours: list[str], num_range: list = None) -> None:

    # Grabs the dictionary of distributions for easy reference
    dists = dist.dists

    # Gets the range for the guessed curve
    if not num_range:
        start, stop, steps = dist.x[0], dist.x[-1], 100
        num_range = [start + i / steps for i in range(int((stop - start) * steps))]

    # Plots each guess distribution
    for guess in dists:

        # Generates the points on the curve
        curve = dist.get_curve(guess, num_range)

        # Plots the curve
        plt.plot(*curve, label = guess, color = colours.pop(0))


        # Logs data
        logger.loga('\ndist params', f'{guess}:')
        for i in range(len(dists[guess]['params'])):
            logger.loga('dist params', f'\t{dists[guess]["params"][i]} ± {dists[guess]["uncs"][i]}')

# Puts a line where the human estimate of π lies
def plot_dataset(dataset: Dataset, colours: list[str]) -> None:
    plt.axvline(x = dataset.live_random.pi, label = f'Human $\pi$: {dataset.live_random.pi:.2f}', color = colours.pop(0), linestyle = 'dashed', linewidth = 0.8)

# Add titles/labels, plus some extra settings
def plot_titles(title: str = None, axes: tuple[str] = None, is_log: bool = False) -> None:
    if title:
        plt.title(title)
    
    if axes:
        plt.xlabel(axes[0])
        plt.ylabel(axes[1])
    
    if is_log:
        plt.xscale('log')

    plt.legend()

# A list of colours.
#   Items are popped from the list to ensure no duplicates.
def get_colours() -> list[str]:
    return list(TABLEAU_COLORS.keys())