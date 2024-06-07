# Functions used to guess at the underlying distribution

import numpy as np
from scipy.special import factorial, gamma as gammaf


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

# A normal distribution, normalised
def normal(x, m, s):
    return (1  / s / np.sqrt(2 * np.pi)) * np.e ** (-0.5 * ((x - m) / s) ** 2)

# A normal distribution, unnormalised
def nonnormal(x, m, s, a):
    return a * np.e ** (-0.5 * ((x - m) / s) ** 2)

# Log-normal
def log_normal(x, m, s):
    return 1 / (x * s * np.sqrt(2 * np.pi)) * np.e ** (-0.5 * (np.log(x - m) / s) ** 2)

# Log-normal, unnormalised
def log_nonormal(x, m, s, a):
    return a / x * np.e ** (-0.5 * (np.log(x - m) / s) ** 2)

# Chi squared
def chi_squared(x, k):
    return 1 / (2 ** (k / 2) * gammaf(k / 2)) * x ** (k / 2 - 1) * np.e ** (-x / 2)

def nochi_squared(x, k, a):
    return a * x ** (k / 2 - 1) * np.e ** (-x / 2)

# Gamma
def gamma(x, k, t):
    return 1 / (gammaf(k) * t ** k) * x ** (k - 1) * np.e ** (-x / t)

def nogamma(x, k, t, a):
    return a * x ** (k - 1) * np.e ** (-x / t)