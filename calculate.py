# Does some calculations

from math import sqrt
from dataset import PairList


# Calculates pi.
#   The chance a random pair of integers are coprime
#   to one another goes as 6 / π^2. Solving for π,
#   then π = sqrt(6 / coprime_fraction)
def find_pi(pairs: PairList) -> float:

    # Calculates the fraction of coprimes in the list
    coprime_fraction = pairs.coprimes / len(pairs)

    # Finds pi
    pi = sqrt(6 / coprime_fraction)

    return pi
