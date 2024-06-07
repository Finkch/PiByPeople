# Does some calculations

from sympy import isprime, sqrt, gcd
from sympy.ntheory import factorint

from numpy import array, kron, ndarray

# Calculates pi.
#   The chance a random pair of integers are coprime
#   to one another goes as 6 / π^2. Solving for π,
#   then π = sqrt(6 / coprime_fraction)
def find_pi(coprimes, pairs) -> float:

    # Calculates the fraction of coprimes in the list
    coprime_fraction = coprimes / pairs

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


# Returns a list of all common factors between two numbers.
#   Implements an approach found on StackExchange.
def cf(a: int, b: int) -> list[int]:
    
    # Finds the gcd of the two numbers
    d = gcd(a, b)

    # Gets all the prime factors in the gcd
    pfs = factorint(d)

    # Using...*ahem*, mixed-radix numbers, iterate through radices.
    #   e.g.: let d = 50 => pfs = 1x2, 2x5
    #   00: 1^0 * 5^0 = 1
    #   01: 1^0 * 5^1 = 5
    #   ... all other combination of range(1 + 1) and range(2 + 1)
    #   12: 1^1 * 5^2 = 50
    #
    #   Since there are an arbitrary amount of pfs, iterate through
    #   all combinations via recursion.
    return cf_recursive(pfs, list(pfs.keys()), [])

def cf_recursive(pfs: dict, keys: list, factors: list) -> list[int]:
    
    # Base case
    if len(keys) == 0:
        return 1
    
    # Takes an item out of the prime factors
    factor = keys.pop()
    radix = pfs.pop(factor)

    # Gets a list of all items l
    for i in range(radix + 1):
        factors.append(
            factor ** i * cf_recursive(pfs, keys, factors)
        )




# The following code is taken from one of my repos: Common-Factors

# Finds the common factors
def cfs(n: int, m: int) -> ndarray[int]:

    # Gets the greatest common denominator
    gcf = gcd(n, m)

    # Gets the prime factors of the gcd
    pfs = factorint(gcf)

    # 1 is always a common factor.
    # We need this to be a non-empty list for
    cfs = array([1], dtype='float64')

    # Recursively finds the common factors by performing
    # the Kronecker product on column matrices composed of
    # mixed radix numbers. In each matrix, there is one
    # base and it contains all values where the radix is
    # equal to or less than the occurances of that
    # base in the prime factorization of the greatest
    # common demoninator.
    #
    # Phew, that's a mouthful!
    return cfs_recursive(pfs, cfs)

# Recursively performs the Kronecker product
def cfs_recursive(pfs: dict, cfs: ndarray) -> ndarray[int]:
    
    # Base cases.
    # Return common factors when there are no
    # more items to perform the Kronecker on
    if len(pfs) == 0:
        return cfs
    
    # Removes an item from the dictionary, getting
    # a base a radix to create a new matrix
    factor, radix = pfs.popitem()

    # Get all items in a mixed radix matrix
    radices = array([factor ** i for i in range(radix + 1)])

    # By performing the Kronecker product on our existing
    # common factors column vector and the mixed radix 
    # matrix, we find more common factors.
    cfs = kron(cfs, radices)

    # Again!
    return cfs_recursive(pfs, cfs)