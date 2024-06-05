# This file makes "random" a black box for other files

from random import seed, randint
from math import pi

# The initial seed
initial_seed = pi


# Constants to determine the range of integers for true random
start_range = 1
end_range = int(1e100)



# Sets the starting seed
def initialise_random():
    seed(initial_seed)

# Selects a random number
def random(start: int = start_range, end: int = end_range):
    return randint(start, end)