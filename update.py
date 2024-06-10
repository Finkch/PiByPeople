# This function is used to automatically updated `README.md`

from distribution import PiDistribution
from generators import human_pi
from show import show_pi
from scipy.stats import norm
import numpy as np

# File names
DF  = '2018'    # Data file
CI  = 'ci'      # Confidence interval file
RM  = 'README'  # README.md


# Gets the ball rolling for the update
def update() -> None:
    
    # Calculates π from human data
    pi = get_pi()

    # Gets the percentile from the bottom this estimate fall in
    score = get_score(pi)

    # Prints everything to console so that it can be piped to README.md
    printout(pi, score)


# Gets an estimate for π and a string to show its error
def get_pi() -> float:
    return PiDistribution(human_pi, None, DF).pi

# Gets the score this estiamte for pi
def get_score(pi: float) -> float:

    # Reads standard deviation from the file
    sd = -1
    with open(f'logs/{CI}.txt', 'r') as file:
        for line in file:
            sd = float(line.strip())
            break

    # Computes the percentile by standardising estimate
    percentile = norm.cdf((pi - np.pi) / sd)

    # Converts to closeness percent from π
    bottom_score = 100 - 2 * abs(percentile - 0.5) * 100
    
    return round(bottom_score, 1)


# Prints README.md so it can be repiped
def printout(pi: float, score: str) -> None:
    
    # Returns pi and some formatting
    #   0: full formatting string
    #   1: float of pi
    #   2: float absolute error
    #   3: float relative error
    #   4: int prevision used for rounded (use `precision - 2` for relative error)
    pif = show_pi(pi)


    # Flavours the score string a bit
    ok = None
    punc = None
    if score > 90:
        ok = 'fantastic'
        punc = '!'
    elif score > 75:
        ok = 'good'
        punc = '!'
    elif score > 50:
        ok  = 'okay'
        punc = '.'
    elif score > 25:
        ok = 'meh'
        punc = '.'
    elif score > 10:
        ok = 'pretty bad'
        punc = '!'
    else:
        ok = 'abysmal'
        punc = '!'

    # The string where π is presented
    pistr = f'**π = {pif[1]:.{pif[4]}f}**, according to humans.  \n'

    # The string where π's errors are presented
    errorstr = f'That\'s off by {pif[2]:.{pif[4]}}, or about {pif[3]:.{pif[4] - 2}f}%!  \n'

    # The string where the score is presented
    scorestr = f'This estimates falls within the bottom {score}% of estimates ({ok}){punc}  \n'

    # Prints out the existing README, substituting several lines
    with open(f'{RM}.md', 'r') as file:
        for line in file:
            if '**π = ' in line:
                print(pistr)
            elif 'That\'s off by ' in line:
                print(errorstr)
            elif 'This estimates falls within the bottom ' in line:
                print(scorestr)
            elif '\n' in line:
                print(line, end = '')
            else:
                print(line)


if __name__ == '__main__':

    # First argument must be data file name (no extension!)
    update()