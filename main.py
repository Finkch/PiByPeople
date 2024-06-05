# Welcome to PiByPeople!
# This is the main file. It get the ball rolling!

from dataset import Dataset

def main():
    
    data_file = '2018'

    dataset = Dataset(f'data/{data_file}.csv')

    print(dataset.live_random.pi)
    print(dataset.semi_random.pi)
    print(dataset.true_random.pi)


# Ensures only the startup thread runs main
if __name__ == '__main__':
    main()