# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from distribution import *
from show import print_pi, plot_distribution, plot

from numpy import average

from logger import logger


def main():
    
    # data_file = '2018'

    # dataset = Dataset(f'data/{data_file}.csv')

    # compare = SmallDistribution(1000, dataset.length * 1000)

    # print_pi(dataset.live_random.pi)
    # print_pi(dataset.semi_random.pi)
    # print_pi(dataset.true_random.pi)
    # print()

    # print(print_pi(average(compare.distribution)))
    # plot_distribution(compare)



    dist = RandomDistribution(factors, 1000, 1e4)

    dist.guess(inverse, 'Inverse', (dist.trials, 1, -1))
    dist.guess(inverse_log, 'Inverse Logarithm', (dist.trials, 1, -1))

    plot(dist)



# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()