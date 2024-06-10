# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from distribution import *
from generators import *
from guesses import *
from show import plot_pi, plot, display
import numpy as np
from logger import logger

# Finds what π is, through human generated values
def piByPeople():
    
    # The file in which data is stored
    data_file = '2018'

    # Loads the dataset
    pi_by_people = PiDistribution(human_pi, None, data_file)

    # Number of trails
    trials = int(1e3)

    # Maximum size of the random number
    max_num = int(1e9)

    # Creates the distribution of π guesses
    dist = RandomDistribution(dist_pi, trials, max_num, pi_by_people.x[0])

    # Gets the percentile in which human π falls.
    #   This has to be called before normalisation.
    score = dist.bottom_percent(pi_by_people.pi, np.pi)

    # Normalise the distribution
    dist.normalise() 

    # Adds some guess curves for the underlying distribution
    dist.guess(normal, 'Normal', (np.pi, 0.25))
    dist.guess(log_nonormal, 'Log-Normal', (2, 0.25, 2))


    # Shows the results
    plot_pi(dist, pi_by_people, score, title='$\pi$ by People', axes=('$\pi$', 'counts (normalised)'))


# For manually testing distributions
def testDistributions():
    
    # Number of trials
    trials = int(1e3)

    # Maximum random number that can be generated
    max_num = 1e6

    # The distribution to test
    dist = RandomDistribution(
        greatest_common_denominator,
        trials,
        max_num
    )

    # Guesses for the distribution
    dist.guess(pareto, 'Pareto\'s', (1, 3))


    # Shows the distribution and the guesses
    plot(dist, is_log = True)
    display(save = False)


# For updates the confidence interval for automatic updates
def updateCI():
    
    trials = int(1e6)

    # Gets human pi
    pi_by_people = PiDistribution(human_pi, None, '2018')

    dist = RandomDistribution(
        dist_pi,            # The distribution
        trials,             # Trials to perform
        int(1e30),          # Max size of random numbers
        pi_by_people.x[0]   # Count of number pairs
    )

    # Finds the percentile in which human π falls
    score = dist.bottom_percent(pi_by_people.pi, np.pi)

    # Logs the score for future reference
    logger.loga('ci', f'{score}')


# Ensures only the startup thread runs main
if __name__ == '__main__':
    
    # piByPeople()

    # testDistributions()

    updateCI()