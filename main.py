# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from distribution import Distribution
from show import print_pi, plot_distribution

from numpy import average

def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')

    distribution = Distribution(100, dataset.length)

    print_pi(dataset.live_random.pi)
    print_pi(dataset.semi_random.pi)
    print_pi(dataset.true_random.pi)
    print()

    print(print_pi(average(distribution.distribution, 0)[0]))
    plot_distribution(distribution)


# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()