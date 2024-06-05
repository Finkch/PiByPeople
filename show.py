# Shows the results

from math import pi


# Returns `π ± unc` with some formatting
def show_pi(guess_pi) -> str:

    # Finds the absolute error
    absolute_error = abs(pi - guess_pi)

    # The relative error
    relative_error = absolute_error / pi * 100

    # The pricision at which to round
    precision = find_rounding(absolute_error)

    # Formats
    abs_pi = f'{guess_pi:.{precision}f} ± {absolute_error:.{precision}f}'
    rel_pi = f'{guess_pi:.{precision}f} ({relative_error:.{precision - 2}f}%)'

    return abs_pi, rel_pi

# Prints out the strings
def print_pi(guess_pi) -> None:
    abs_pi, rel_pi = show_pi(guess_pi)
    print(f'{abs_pi}\t\t{rel_pi}')


# Find the pricision at which to round.
#   This shows one more digit than it should for
#   showing uncertainty, but there is no fund to
#   be found is showing such truncated numbers.
def find_rounding(error: float) -> int:
    i = 0
    while error <= 1:
        error *= 10
        i += 1

    return i + 1




    
