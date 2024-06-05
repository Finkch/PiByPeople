# Does some calculations

from math import sqrt, gcd
from sympy import isprime


# Calculates pi.
#   The chance a random pair of integers are coprime
#   to one another goes as 6 / π^2. Solving for π,
#   then π = sqrt(6 / coprime_fraction)
def find_pi(pairs) -> float:

    # Calculates the fraction of coprimes in the list
    coprime_fraction = pairs.coprimes / len(pairs)

    # Finds pi
    pi = sqrt(6 / coprime_fraction)

    return pi


# Determines whether the pair is coprime.
#   A pair of numbers are coprime iff their greatest
#   common demoninator (gcd) is 1.
def is_coprime(pair) -> 0 | 1:
    return 1 if gcd(*pair) == 1 else 0


# Checks if a number is prime.
def is_prime(n: int) -> 0 | 1:
    return 1 if isprime(n) else 0
