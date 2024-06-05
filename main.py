# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset
from show import print_pi

def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')



    print_pi(dataset.live_random.pi)
    print_pi(dataset.semi_random.pi)
    print_pi(dataset.true_random.pi)


# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()