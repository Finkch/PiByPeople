# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from calculate import find_pi

def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')

    live_pi = find_pi(dataset.live_random)
    semi_pi = find_pi(dataset.semi_random)
    true_pi = find_pi(dataset.true_random)

    print(live_pi)
    print(semi_pi)
    print(true_pi)


# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()