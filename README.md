# PiByPeople

`TODO: Insert π here`

## Introduction

This project began over half a decade ago when I had a question: just how bad are people at being truly random? After I had learned of a brilliant maths theorem that relates pairs of random numbers to a calculation of π (thanks, [Matt Parker](https://www.youtube.com/watch?v=RZBhSi_PwHU)!), I had found an empirical way to test human randomness.

This project calculates the mathematical constant π, poorly. It does so by comparing pairs of human-generated random values to see whether or not they are coprime to one another; the odds of a pair of random integers being coprime go to six by π squared. Strictly speaking, this identiy is only true in the limit as the sample size goes to infinity and if the range of random numbers is `[0, infinity)`.

While I said that this project started over half a decade ago, it was no more than a spreadsheet sitting on my computer until roughly a week before I wrote this. In that time, one would expect I would have gathered more than 25 pairs of numbers from people, but I don't exactly go to parties to perform interrigations about random numbers.


## Comparing to Other Randomness

To see how close human random gets to the true value of π, this repository runs an experiment. It generates *n* distributions of equal size to the list of number pairs sumbitted by humans. By comparing the human generated estimate for π against those created from the *n* distributions, we can find just how good or poor humans are at being random.

In this experiemnt, *n* equals 10 000 since that's a reasonable size for my computer to go through in about a minute. Together, the *n* distributions form a greater distribution that is roughly normal (it's closer to log-normal or beta, especially when the size of each distribution is small). Since we take a large number of samples, it's reasonable to assume that sample distribution approaches the true distribution.


## Try it at Home

This is intended to be a small project. While I do not want to crowd source my random numbers, I highly encourage others to toy around with this theorem to play with randomness in a fun context. The core concept makes for a great introductory assignment for an amateur coder. As for my list of human generated values, I want to very carefully elicit submissions from participants - by the simple act of asking for a random number, one influences the volunteer's output.

If you want to try this experiment yourself, clone the repository. Then all you have to do is either overwrite the data file (`data/2018.csv`) or add your own data file and adjust the code to point at it (`main.py` in `piByPeople()`, change `2018` the the name of your file, excluding the extension). If you add your own data file, make sure it follows the same formatting, unless you want to rewrite `file_generator()` in `generators.py`; the formatting is a csv file where the first two columns contain the number pairs.
