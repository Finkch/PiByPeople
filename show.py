# Shows the results

import matplotlib.pyplot as plt
from matplotlib.colors import TABLEAU_COLORS
from numpy import pi, average

from distribution import RandomDistribution, PiDistribution

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
    pistr = f'{guess_pi:.{precision}f} ± {absolute_error:.{precision}f} ({relative_error:.{precision - 2}f}%)'

    return pistr, guess_pi, absolute_error, relative_error, precision

# Prints out the strings
def print_pi(preamble: str, guess_pi: float) -> None:
    print(preamble, end = '')
    guess_pi = show_pi(guess_pi)[0]
    print(f'{guess_pi}\n')


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




# Plots normally, but also does some extra for π
def plot_pi(dist: RandomDistribution, pi_by_people: PiDistribution, score: str, num_range: list = None, title: str = None, axes: tuple[str] = None, is_log: bool = False, save: bool = False):

    # Prints the human estimate for π
    print_pi('Human estimate:\n\t', pi_by_people.pi)

    # Prints the mean and median estimates for π
    print_pi('Mean of random distributions:\n\t', average(dist.x, weights = dist.y))

    # Prints the normal distribution's estimate for π
    print_pi('Normal distribution\'s mean:\n\t', dist.dists['Normal']['params'][0])
    
    # Prints the percentile of how close to true π the human
    # estimate falls. Do note that values at clamped to
    # [1, 50] for clarirty.
    if score > 50:
        print(f'The human estimate of π falls in the top {max(int(100 - score), 1)}% of values!\n')
    else:
        print(f'The human estimate of π falls in the bottom {max(int(score), 1)}% of values!\n')

    # Plots
    colours = plot(dist, num_range, title, axes, is_log)
    plot_dataset(pi_by_people, colours)
    display(save)
    


# Plots a random distribution and the guesses underlying it
def plot(dist: RandomDistribution, num_range: list = None, title: str = None, axes: tuple[str] = None, is_log: bool = False):

    # Gets the points for the random distribution
    points = (dist.x, dist.y)

    # Gets a list of colours to use
    colours = get_colours()

    # Gets the range on which to plot the guess curves
    if not num_range:
        num_range = dist.range()
        
    # Plots the random distribution data
    plot_scatter(points, colours)
    plot_guesses(dist, colours, num_range = num_range)

    # Finishing touches
    plot_titles(title, axes, is_log)

    return colours

# Plots the distribution
def plot_scatter(points: tuple, colours: list[str]) -> None:
    plt.scatter(*points, color = colours.pop(0), label = 'Random Distributions')

# Plots the theoretical distribution
def plot_guesses(dist: RandomDistribution, colours: list[str], num_range: list = None) -> None:

    # Grabs the dictionary of distributions for easy reference
    dists = dist.dists

    # Plots each guess distribution
    for guess in dists:

        # Generates the points on the curve
        curve = dist.get_curve(guess, num_range)

        # Plots the curve
        plt.plot(*curve, label = guess, color = colours.pop(0))


        # Logs data
        logger.loga('params', f'\n{guess}:')
        for i in range(len(dists[guess]['params'])):
            logger.loga('params', f'\t{dists[guess]["params"][i]} ± {dists[guess]["uncs"][i]}')

# Puts a line where the human estimate of π lies
def plot_dataset(pi_by_people: PiDistribution, colours: list[str]) -> None:
    plt.axvline(x = pi_by_people.pi, label = f'Human $\pi$: {pi_by_people.pi:.2f}', color = colours.pop(0), linestyle = 'dashed', linewidth = 0.8)

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

def display(save: bool = False):
    if not save:
        plt.show()
    else:
        plt.savefig()