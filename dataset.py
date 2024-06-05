# Contains the data set

from read import read
from numpy import array
from random_numbers import random, initialise_random
import datetime

class Dataset:

    def __init__(self, file_path: str) -> None:

        self.live_random, self.metadata = read(file_path)

        # Extracts information for easy reference
        # Generators are because column splicing keeps one too many lists
        self.pseudonyms = [item[0] for item in self.metadata[:,:1]]
        self.times      = [item[0] for item in self.metadata[:,1:2]]
        self.acks       = [item[0] for item in self.metadata[:,2:]]

        self.pairs      = len(self.live_random)

        self.semi_random = self.generate_semi_random()
        self.true_random = self.generate_true_random()

        
        self.coprimes   = 0
        self.primes     = 0

    def generate_semi_random(self) -> list[list[int, int]]:

        semi_random = []        

        for i in range(self.pairs):

            # The first number is generated via the acknowledgement
            # It's the sum of ASCII values
            a = sum([ord(letter) for letter in self.acks[i]])

            # The second number converts time of day to a number
            # Append the line number as seconds
            timestamp = f'{self.times[i]}:{i % 60}'

            timestamp = datetime.datetime.strptime(timestamp, '%H:%M:%S')

            delta = timestamp - datetime.datetime(1900, 1, 1)
            b = delta.total_seconds()
            
            
            # semi_random will have the same dimensions as live_random
            semi_random.append(array([a, b]))
        return array(semi_random)
        

    def generate_true_random(self) -> list[list[int, int]]:
        
        # Sets the seed to some number
        initialise_random()

        # Calls random numbers to fill the array
        # true_random will have the same dimensions as live_random
        return array([
            array([
                random(), random()
            ]) for i in range(self.pairs)
        ])