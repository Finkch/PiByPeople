# Does some calculations

from math import sqrt


# Calculates pi.
#   The chance a random pair of integers are coprime
#   to one another goes as 6 / π^2. Solving for π,
#   then π = sqrt(6 / coprime_fraction)
def find_pi(nums: list) -> float:

    # Gets the number of coprime pairs in the list of nums
    coprimes = sum([pair.coprime for pair in nums])

    # Gets the total amount of pairs in the list
    entries = len(nums)

    # Calculates the fraction of coprimes in the list
    coprime_fraction = coprimes / entries

    # Finds pi
    pi = sqrt(6 / coprime_fraction)

    return pi
