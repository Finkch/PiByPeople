# Contains the data set

from read import read
from random_numbers import random, initialise_random
from datetime import datetime
from math import gcd

class Dataset:

    def __init__(self, file_path: str) -> None:

        # Gets the data from the file
        self.live_random, self.metadata = read(file_path)

        # Converts live_random to a list of Pairs
        self.live_random = [Pair(pair[0], pair[1]) for pair in self.live_random]


        # Extracts information for easy reference
        # Generators are because column splicing keeps one too many lists
        self.pseudonyms  = [item[0] for item in self.metadata[:,:1]]
        self.times       = [item[0] for item in self.metadata[:,1:2]]
        self.acks        = [item[0] for item in self.metadata[:,2:]]

        # Gets the number of pairs
        self.pairs       = len(self.live_random)

        # Generates other pairs of numbers
        self.generate_semi_random()
        self.generate_true_random()

        # Count of pairs of coprime numbers
        self.coprimes   = 0

        # Count of prime numbers
        self.primes     = 0

    # Generates a list of semi-random numbers from the
    # metadate of each entry
    def generate_semi_random(self):

        self.semi_random = []        

        for i in range(self.pairs):

            # The first number is generated via the acknowledgement
            # It's the sum of ASCII values
            a = sum([ord(letter) for letter in self.acks[i]])

            # The second number converts time of day to a number
            # Append the line number as seconds
            timestamp = f'{self.times[i]}:{i % 60}'

            # Finds the time since the start of the day
            delta = datetime.strptime(timestamp, '%H:%M:%S') - datetime(1900, 1, 1)

            # Converts the time to a number that's easier to work with
            b = delta.total_seconds()
            
            
            # semi_random will have the same dimensions as live_random
            self.semi_random.append(Pair(a, b))
        

    # Generates a list of 'true' (computer) random numbers
    def generate_true_random(self):
        
        self.true_random = []

        # Sets the seed to some number
        initialise_random()

        # Calls random numbers to fill the array
        # true_random will have the same dimensions as live_random
        self.true_random = [Pair(random(), random()) for i in range(self.pairs)]




# A pair of numbers
class Pair:
    def __init__(self, a: int, b: int) -> None:
        self.a = int(a)
        self.b = int(b)

        self.pair = [self.a, self.b]

        self.coprime = self.is_coprime()

    def __str__(self):
        return f'({self.a}, {self.b})'

    def __getitem__(self, i):
        return self.pair[i]
    
    # Determines whether the pair is coprime.
    #   A pair of numbers are coprime iff their greatest
    #   common demoninator (gcd) is 1.
    def is_coprime(self) -> 0 | 1:
        return 1 if gcd(*self.pair) == 1 else 0