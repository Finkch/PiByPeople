# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

# TODO:
#   Test performance of double gcd == 1
#       Reimplement gross RandomDist of RandomDistss and add it to test


from dataset import Dataset
from distribution import *
from generators import *
from guesses import *
from show import plot


def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')


    # dist = RandomDistribution(factors, 10000, 1e5)
    # dist = RandomDistribution(common_factors, 10000, 1e100)
    # dist = RandomDistribution(greatest_common_denominator, 10000, 1e100)
    # dist = RandomDistribution(gcd_is_n, 10000, 1e100, 1)

    # dist = RandomDistribution(dist_gcd_is_n, 100, 1e3, dataset.length, 1)
    # dist = RandomDistribution(dist_dist_gcd_is_n, 100, 1e3, dataset.length, 1, final_step = lambda d: ([sqrt(6 / (d.y / d.args[1]))], [1]))
    
    dist = RandomDistribution(dist_pi, 10000, 1e3, dataset.length)
    

    # dist.guess(inverse, 'Inverse', (dist.trials, 1, -1))
    # dist.guess(inverse_log, 'Inverse Logarithm', (dist.trials, 1, -1))

    plot(dist)





# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()