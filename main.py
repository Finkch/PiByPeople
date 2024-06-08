# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from distribution import *
from generators import *
from guesses import *
from show import plot_pi
import numpy as np

def PiByPeople():
    
    # The file in which data is stored
    data_file = '2018'

    # Loads the dataset
    piByPeople = PiDistribution(human_pi, None, data_file)

    # Number of trails
    trials = 1000

    # Maximum size of the random number
    max_num = 1e9

    # Creates the distribution of π guesses
    dist = RandomDistribution(dist_pi, trials, max_num, piByPeople.x[0])

    # Gets the percentile in which human π falls.
    #   This has to be called before normalisation.
    # score = dist.bottom_percent(dataset.live_random.pi, np.pi)
    score = dist.bottom_percent(piByPeople.pi, np.pi)

    # Normalise the distribution
    dist.normalise() 

    # Adds some guess curves for the underlying distribution
    dist.guess(normal, 'Normal', (np.pi, 0.25))
    dist.guess(log_nonormal, 'Log-Normal', (2, 0.25, 2))

    # Shows the results
    plot_pi(dist, piByPeople, score, title='$\pi$ by People', axes=('$\pi$', 'counts (normalised)'))




# Ensures only the startup thread runs main
if __name__ == '__main__':
    PiByPeople()