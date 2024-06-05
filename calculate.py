# Does some calculations

from math import sqrt, gcd


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
#   Employs the "6k ±1" algorithm.
def is_prime(n: int) -> 0 | 1:
    
    # One and zero are both non-prime
    if n <= 1:
        return 0
    
    # Two and three are prime
    if n <= 3:
        return 1
    
    # Checks divisible by two and by three
    if n % 2 == 0 or n % 3 == 0:
        return 0
    
    # Checks of the form 6k ± 1
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return 0
        i += 6

    return 1
