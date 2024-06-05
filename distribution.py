# Uses random distributions to determine just how bad
# the humans did at generating pi.

from random_numbers import random, initialise_random
from numpy import array
from dataset import PairList


# Generates lots of PairLists of random numbers to
# create a distribution.
class Distribution:
    def __init__(self, trials: int, length: int) -> None:
        
        # The count of items in the distribution
        self.trials = trials

        # The count of number pairs per trial
        self.length = length

        # Rather than holding PairLists, discards
        # the numbers themselves but keeps π,
        # coprime count, and prime count.
        self.distribution = self.generate()


    # Creates the data for the distribution
    def generate(self) -> None:

        # Sets seed via system time (or OS specific random)
        initialise_random(None)        

        distribution = []
        for i in range(self.trials):

            # Generates the random data for a single trial
            pairs = PairList([[random(), random()] for j in range(self.length)])

            # Adds the relevant information to the distribution
            distribution.append([
                pairs.pi,
                pairs.coprimes,
                pairs.primes
            ])

        # Converts the list to a numpy array        
        return array(distribution)