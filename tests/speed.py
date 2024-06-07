# Compares several functions' performance

from distribution import *

# This test is defunct
# Distribution tests
# def test_distributions(trials):
#     args = [
#         100,
#         100
#     ]
#
#     return args, [create_dist, create_sdist, create_ssdist, create_sdist_trials, create_sdist_length], ['dist', 'sdist', 'ssdist', 'trials dist', 'length dist'], False


# Generator tests
def test_gcd_is_n(trials):
    args = [
        100,
        100,
        1e5
    ]

    #return args, [gcdisn_small, gcdisn_rd, gcdisn_distrd], ['Small Dist', 'Random Dist', 'Random Dist Dist'], False
    return args, [gcdisn_distrd], ['Random Dist'], False


'''     Distribution findings

Small distributions are ~10x faster.

Increasing length is marginally better for performance than
increasing trials.

Changing the max random number has minimal effect on sdists.

'''
# def create_dist(trials, length):
#     dist = Distribution(trials, length)

# def create_sdist(trials, length):
#     dist = SmallDistribution(trials, length)

# def create_ssdist(trials, length):
#     dist = SmallDistribution(trials, length, int(1e100))

# def create_sdist_trials(trials, length):
#     dist = SmallDistribution(trials * 10, length)

# def create_sdist_length(trials, length):
#     dist = SmallDistribution(trials, length * 10)




'''     Generators findings

Turns out they are all comperable to one another. There is only
a ~5% difference between each of these implementations. That said,
SmallDistribution is the fastest and RD of RDs is the slowest.

'''
# def gcdisn_small(trials, length, max_num):
#     dist = SmallDistribution(trials, length, max_num)

# Function removed
# def gcdisn_rd(trials, length, max_num):
#     dist = RandomDistribution(dist_gcd_is_n, trials, max_num, length, 1)

def gcdisn_distrd(trials, length, max_num):
    dist = RandomDistribution(dist_dist_gcd_is_n, trials, max_num, length, 1)