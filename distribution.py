# Uses random distributions to determine just how bad
# the humans did at generating pi.

from random_numbers import random, initialise_random
from numpy import array, histogram, sqrt, pi, ndarray, log10
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

    # Generates a bunch of distributions
    def generate(self):

        # Sets the seed using system time
        initialise_random(None)

        dist = []
        for i in range(self.trials):
            
            # Gets the data for a single distribution.
            # We only care about the coprimes, for performance reasons
            coprimes = sum([
                is_coprime(
                    [random(end=1e5), random(end=1e5)] # Pairs of random numbers!
                ) for j in range(self.length)
            ])

            dist.append(coprimes)


        # Calculates π
        pis = sqrt(6 / array(dist) * self.length)

        return pis
    
    # Creates a numpy histogram of the distribution data
    def histogram(self, bin_size: float = None) -> tuple[ndarray, ndarray, float]:

        if not bin_size:
            bin_size = 1 / sqrt(self.length)


        # Gets a bunch of reasonably sized bins
        bins = [pi + bin_size * (i - 0.5) for i in range(-30, 30)]

        y, x = histogram(self.distribution, bins)

        logger.log('dist print', [str(datum) for datum in x] + ['\n\n'] + [str(datum) for datum in y])

        # Grabs the histogram, trimming of excess zeroes
        x, y = self.trim_histogram(y, x)

        x += bin_size / 2

        return x, y, bin_size


    # Removes excess zereos.
    #   NOTE: the order is (y, x), the return order for np.histogram()
    def trim_histogram(self, y: ndarray, x: ndarray) -> tuple[ndarray]:
        
        # Finds the last leading zero
        start = 0
        for i in range(len(y)):
            if y[i] != 0:
                start = i
                break
        
        # Finds the first trailing zero
        stop = 0
        for i in range(len(y) - 1, 0, -1):
            if y[i] != 0:
                stop = i + 1
                break

        print(f'Slicing!:\t{start} : {stop}')

                
        # Trims and returns the arrays
        return x[start : stop], y[start : stop]

        
        