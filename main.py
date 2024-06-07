# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from distribution import *
from generators import *
from guesses import *
from show import plot
import numpy as np

def main():
    
    # The file in which data is stored
    data_file = '2018'

    # Loads the dataset
    dataset = Dataset(f'data/{data_file}.csv')

    # Number of trails
    trials = 1000

    # Maximum size of the random number
    max_num = 1e9

    # Creates the distribution of π guesses
    dist = RandomDistribution(dist_pi, trials, max_num, dataset.length)
    dist.normalise() # Normalise!

    # Adds some guess curves for the underlying distribution
    dist.guess(normal, 'Normal', (np.pi, 0.25))
    dist.guess(log_nonormal, 'Log-Normal', (2, 0.25, 2))

    # Shows the results
    plot(dist, dataset, title='$\pi$ by People', axes=('$\pi$', 'counts (normalised)'))




# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()