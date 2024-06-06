# Compares several functions' performance

from distribution import *


def test_distributions(trials):
    args = [
        100,
        100
    ]

    return args, [create_dist, create_sdist, create_ssdist, create_sdist_trials, create_sdist_length], ['dist', 'sdist', 'ssdist', 'trials dist', 'length dist'], False


'''     Distribution findings

Small distributions are ~10x faster.

Increasing length is marginally better for performance than
increasing trials.

Changing the max random number has minimal effect on sdists.

'''
def create_dist(trials, length):
    dist = Distribution(trials, length)

def create_sdist(trials, length):
    dist = SmallDistribution(trials, length)

def create_ssdist(trials, length):
    dist = SmallDistribution(trials, length, int(1e100))

def create_sdist_trials(trials, length):
    dist = SmallDistribution(trials * 10, length)

def create_sdist_length(trials, length):
    dist = SmallDistribution(trials, length * 10)
