# PiByPeople

**π = NAN**, according to humans.  

That's off by NAN, or about NAN%!  

This estimates falls within the bottom NAN% of estimates (NAN)NAN  


## Introduction

This project began over half a decade ago when I had a question: just how bad are people at being truly random? After I had learned of a brilliant maths theorem that relates pairs of random numbers to a calculation of π (thanks, [Matt Parker](https://www.youtube.com/watch?v=RZBhSi_PwHU)!), I had found an empirical way to test human randomness.

This project calculates the mathematical constant π, poorly. It does so by comparing pairs of human-generated random values to see whether or not they are coprime to one another; the odds of a pair of random integers being coprime go to six by π squared. Strictly speaking, this identiy is only true in the limit as the sample size goes to infinity and if the range of random numbers is `[0, infinity)`.

While I said that this project started over half a decade ago, it was no more than a spreadsheet sitting on my computer until roughly a week before I wrote this. In that time, one would expect I would have gathered more than 25 pairs of numbers from people, but I don't exactly go to parties to perform interrigations about random numbers.


## Comparing to Other Randomness

To see how close human random gets to the true value of π, this repository runs an experiment. It generates *n* distributions of equal size to the list of number pairs sumbitted by humans. By comparing the human generated estimate for π against those created from the *n* distributions, we can find just how good or poor humans are at being random.

In this experiemnt, *n* equals 10 000 since that's a reasonable size for my computer to go through in about a minute. Together, the *n* distributions form a greater distribution that is roughly normal (it's closer to log-normal or beta, especially when the size of each distribution is small). Since we take a large number of samples, it's reasonable to assume that sample distribution approaches the true distribution.


## Try it at Home

This is intended to be a small project. While I do not want to crowd source my random numbers, I highly encourage others to toy around with this theorem to play with randomness in a fun context. The core concept makes for a great introductory assignment for an amateur coder. As for my list of human generated values, I want to very carefully elicit submissions from participants - by the simple act of asking for a random number, one influences the volunteer's output.

If you want to try this experiment yourself, clone the repository. Then all you have to do is either overwrite the data file (`data/2018.csv`) or add your own data file and adjust the code to point at it ([`main.py`](#mainpy) in `piByPeople()`), change `2018` the the name of your file, excluding the extension). If you add your own data file, make sure it follows the same formatting, unless you want to rewrite `file_generator()` in [`generators.py`](#generatorspy); the formatting is a csv file where the first two columns contain the number pairs.


## Files and Directories

Below are a list of all the files and directories with a brief explanation of each. If you want more details, look at the comments in its respective file.


### data

The `data` directory is where datasets are stored. These datasets contain pairs of non-zero, positive integers generated by people. In the base repository, there is only one–`2018.csv`–which contains the set of numbers I have elicited from participants.

The format of the data files must be a csv file where the first two columns are non-zero, positive integers.


### logs

The `logs` directory contains txt file genereted by the `logger`, contained within `logger.py`. While this directory is mostly used to debugging information, it also contains the best-fit parameters for the guess curves in the `params.txt` file (see [`guesses.py`](#guessespy) for more on guess curves) and data used for [automatic updates](Auto Updates) in `ci.txt`. `ci.txt` is only updated when `updateCI()` is manually called in [`main.py`](#mainpy).


### .github/workflows

The `.github/workflows` directory contains a single file: `autoupdate.yml`. This file is used by a GitHub Actions runner to keep this file up to date (see: [Auto Updates](#auto-updates)).


### main.py

The `main.py` file starts the program for human users. It has three possible execution paths, `piByPeople()`, `testDistributions()`, and `updateCI()` (to select, comment/uncomment at the bottom of the file).

`piByPeople()` runs the experiment mentioned in the [introduction](#introduction). It calcualtes π from the pairs in the data file, creates *n* random distributions, and compares the random distributions to the human created one. Best-fit normal and log-normal curves are shown and the results are plotted.

`testDistributions()` is for playing around with various distributions and guess curves (see [`guesses.py`](#guessespy) for more on guess curves). For example, the default setting is a random distribution is created from 1000 trials of the greatest common denominator (see [`generators.py`](#generatorspy)) between a pair of random numbers. The Pareto distribution is applied as a guess curve. The experimental data and the best-fit Pareto distribution are plotted.

`updateCI()` is used for [automatic updates](#auto-updates) to update the confidence interval of the *n* distributions to find π experimentally; this data is stored in [`logs/ci.txt`](#logs). The *n* used here is greater than the *n* in `piByPeople()`, as this function does not need to run live.

There are other files to start this program and they are used for [automatic updated](#auto-updates) of this `README.md` file. The other entry points are described in [update.py](#updatepy).


### distribution.py

The `distribution.py` file contains three classes that embody a distribution of numbers. These three classes are fundemantal to this repositroy and work in tandem with [`generator.py`](#generatorspy) and [`guesses.py`](#guessespy).


#### Distribution

The `Distribution` class is used for exact distributions, that is a dsitribtion created by an equation and not by an experiemnt. It is used to generate a series of `(x, y)` points to be plotted. The other two classes (`RandomDistribution` and `PiDistribution`) can contain multiple `Distribution` as guesses (see [`guesses.py`](#guessespy)).


#### RandomDistribution
The `RandomDistribution` class is used to experimentally generate a distribution. After being given a generator (see [`generator.py`](#generatorspy)), it will run the experiment to create a sereis of `(x, y)` points that can be plotted. For most of the generators, the `(x, y)` points will take the form of a histogram. As a note, the generator can generate `RandomDistribution`s to find the mean of the experiments.  
`RandomDistribution` also contains plenty of helper functions, such as returning the percentile in which a given value falls.


#### PiDistribution

The `PiDistribution` is used by `piByPeople()` in [`main.py`](#mainpy) to run the primary experiment. `PiDistribution` extends `RandomDistribution`. The main difference between `PiDistribution` and `RandomDistribution` is that after `PiDistribution` generates its data, it transforms the y-data (a single value representing the number of coprimes) into an estimate for π.


### generators.py

The `generators.py` file contains functions to generate numbers. These functions are given to a [`RandomDistribution`](#randomdistribution) to generate values to create the distribution. For example, `common_factors()` returns a list of common factors between a pair of random numbers; the [`RandomDistribution`](#randomdistribution) that own `common_factors()` will call it a number of times equal to how many trails it will perform.  

Generators are split into generic generators and speficic generators. A specific generator returns a generic generator with (typically) an anonymous function as an argument. The anonymous argument is called by the generic generator to actually generate data for a single trial. The generic generator then aggregates the data from each trial and composes it into `x` and `y` data. This is done as the [`RandomDistribution`](#randomdistribution) that owns the generator calls the generator a single time while allowing the generator to decide how its data is aggregated.


### guesses.py

The `guesses.py` file contains functions that contain mathematical equations describing a type of distribution or curve. These so-called guesses are given to a [`RandomDistribution`](#randomdistribution) to try to model the underlying true distribution. Specifically, the [`RandomDistribution`](#randomdistribution) performs an optimising curve fit of the function on its own data and creates a [`Distribution`](#distribution) to store the information. When the [`RandomDistribution`](#randomdistribution) is plotted, the [`Distribution`s](#distribution) containing the guesses are also plotted.

Most guesses have have simple form (function has the "simple_" prefix) which contains a minimal subset of parameters as well as a "non-normal" form (no prefix; standard form). The the data is not necessarily normalised, or otherwise does not represent a probability density function, it is useful to have additional parameters to scale or offset the guesses.


### show.py

The `show.py` file plots and prints. If `plot()` given a [`RandomDistribution`](#randomdistribution), it will plot its data as well as its guesses (see: [`guesses.py`](#guessespy)). Similarly, if `plot_pi()` is given a [`PiDistribuion`](#pidistribution), it will plot the distribution as well as the human estimate for π, then print out the associated errors.


### random_numbers.py

The `random_number.py` file is responsible for generator random numbers. It is little more than a wrapper for Python's random.randit function, mostly because I wanted there to be room to adjust the underlying random generator without affecting the rest of the program.


### calculate.py

The `calculate.py` file contains several mathematical functions that did not fit elsewhere.


### logger.py

The `logger.py` file contains the `Logger` class and a global instance of the object (known as `logger`). This class is used to log data to files. The prinary use-case for the `logger` was for debugging but it also captures the best-fit parameters from guesses in `params.txt` (see: [`guesses.py`](#guessespy)) and outputs data in `ci.txt` for [automatic updates](#auto-updates) of this here `README.md`.


### performance.py

The `performance.py` file contains a simple framework to test the performance of a function. A test is run by supplying `run_test()` with a test-case function and the number of trials to perform; the results are returned as a list of strings.

A single test-case returns in order: a tuple containing the arguments for the functions to test, a tuple of functions to test, a tuple of the string names for the functions, and a bool for whether each trial gets unique parameters. 


### performance_tests.py

The `performance_tests.py` file contains test-cases for [`performance.py`](#performancepy). Most tests have been commented out since their functions were removed or depracated; after I ran the tests, I moved the implementation to focus on the best performer.

A single test-case returns in order: a tuple containing the arguments for the functions to test, a tuple of functions to test, a tuple of the string names for the functions, and a bool for whether each trial gets unique parameters. 


### update.py

The `update.py` file is used to keek this `README.md` file [up to date](#auto-updates) with the current human estimate for π. It is called by a GitHub Actions runner and does three things: reads the data file to generate human π, finds where on the confidence interval the human π falls, and then writes that data to this `README.md`.


## Auto Updates

This `README.md` file is automatically updated whenever the `data` branch on GitHub recieves a push. The `data` branch is used exclusively to update [dataset files](#data). Using GitHub Actions, a Python script is executed to first find the new human generated estiamted for π before using it to update this file. The YAML script to perform this auto update is contained in [`.github/workflows/autoupdate.yml`](#githubworkflows)
