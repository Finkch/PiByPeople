# Uses random distributions to determine just how bad
# the humans did at generating pi.

from random_numbers import random, initialise_random
from numpy import array, histogram, sqrt
from dataset import PairList
from calculate import is_coprime
from logger import logger


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
    def generate(self):

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

    # Returns a histogram of the pi data    
    def histogram(self) -> tuple:        
        return histogram(self.distribution[:,0])
    

# Runs much faster than regular distribution, but less useful.
#   Used for generating histogram.
class SmallDistribution:
    def __init__(self, trials: int, length: int, max_num = 1e5) -> None:
        self.trials = trials
        self.length = length

        self.distribution = self.generate()

    def generate(self):
        initialise_random(None)
        dist = []

        for i in range(self.trials):
            
            coprimes = sum([
                is_coprime(
                    [random(end=1e5), random(end=1e5)]
                ) for j in range(self.length)
            ])

            dist.append(coprimes)



        
        pis = sqrt(6 / array(dist) * self.length)
        
        for i in range(self.trials):
            logger.loga('copris', f'{i}:\t{dist[i]} --> {pis[i]}')

        logger.loga('copris', '\n\n----------\n\n')

        return pis
    
    def histogram(self) -> tuple:
        return histogram(self.distribution)

        
        