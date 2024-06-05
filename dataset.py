# Contains the data set

from read import read
from random_numbers import random, initialise_random
from calculate import is_prime, is_coprime, find_pi

from datetime import datetime

from logger import logger

class Dataset:

    def __init__(self, file_path: str) -> None:

        # Gets the data from the file
        self.live_random, self.metadata = read(file_path)

        # Converts live_random to a list of Pairs
        self.live_random = PairList(self.live_random)


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

        semi_random = []        

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
            semi_random.append((a, b))
        self.semi_random = PairList(semi_random)
        

    # Generates a list of 'true' (computer) random numbers
    def generate_true_random(self):
        
        self.true_random = []

        # Sets the seed to some number
        initialise_random()

        # Calls random numbers to fill the array
        # true_random will have the same dimensions as live_random
        self.true_random = PairList([(random(), random()) for i in range(self.pairs)])


# A pair of numbers
class Pair:
    def __init__(self, a: int, b: int) -> None:
        self.a = int(a)
        self.b = int(b)

        self.pair = (self.a, self.b)

        self.coprime = is_coprime(self)
        self.primes = sum([is_prime(self.a), is_prime(self.b)])

    def __str__(self) -> str:
        return f'({self.a}, {self.b}):\tCoprime {self.coprime}, primes {self.primes}'

    def __getitem__(self, item) -> int:
        return self.pair[item]
    
    

# A list of pairs
class PairList:
    def __init__(self, pairs: list[list[int, int]]) -> None:
        self.pairs = [Pair(*pair) for pair in pairs]

        self.coprimes = self.count_coprimes()
        self.primes = self.count_primes()

        self.pi = find_pi(self)

    # Magic methopds
    def __getitem__(self, item) -> Pair:
        return self.pairs[item]
    
    def __len__(self) -> int:
        return len(self.pairs)
    
    def __str__(self) -> str:
        return ''.join([f'{pair}\n' for pair in self.pairs])
    

    # Functions to aggregate stats
    def count_coprimes(self) -> int:
        return sum([pair.coprime for pair in self.pairs])
    
    def count_primes(self) -> int:
        return sum([pair.primes for pair in self.pairs])
