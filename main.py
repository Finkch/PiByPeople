# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from distribution import Distribution, SmallDistribution
from show import print_pi, plot_distribution

from numpy import average

from logger import logger


def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')

    compare = SmallDistribution(1000, dataset.length * 1000)

    print_pi(dataset.live_random.pi)
    print_pi(dataset.semi_random.pi)
    print_pi(dataset.true_random.pi)
    print()

    print(print_pi(average(compare.distribution)))
    plot_distribution(compare)



# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()