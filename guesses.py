# Functions used to guess at the underlying distribution

import numpy as np
from scipy.special import factorial


# An inverse with plenty of arguments
def inverse(x, a, b, c):
    return a / (x - c) + b

# An inverse with few arguments 
def simple_inverse(x, a):
    return a / x

# A Poisson distribution
def poisson(x, l, a):
    return a * ((l ** x) * (np.e ** -l)) / factorial(x)

# An inverse logarithm
def inverse_log(x, a, b, c):
    return a / np.log(x + b) + c