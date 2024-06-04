# PiByPeople

`TODO: Insert π here`

## Introduction

This project began over half a decade ago when I had a question: just how bad are people at being truly random? After I had learned of a brilliant maths theorem that relates pairs of random numbers to a calculation of π (thanks, [Matt Parker](https://www.youtube.com/watch?v=RZBhSi_PwHU)!), I had found an empirical way to test human randomness.

This project calculates the mathematical constant π, poorly. It does so by comparing pairs of human-generated random values to see whether or not they are coprime to one another; the odds of a pair of random integers being coprime go to six by π squared. `TODO: add LateX for pretty equations`


## Comparing to Other Randomness

Simultaneosuly to humans unwittingly generating π through sumbitting random numbers, this project generates π in other (hopefully) more random methods. The two other methods employ the same theorem but source their random numbers elsewhere. Namely, a pair of random numbers derived from metadata of a human submission `TODO: elaborate on what the previous means` and a pair of 'true' random numbers, as per Python3's `random` libray `TODO: check other Python3 libraries for best source of 'true' randomness`.


## Try it at Home

This is intended to be a small project. While I do not want to crowd source my random numbers, I highly encourage others to toy around with this theorem to play with randomness in a fun context. The core concept makes for a great introductory assignment for an amateur coder. As for my list of human-generated values, I want to very carefully elicit submissions from participants - by the simple act of asking for a random number, one influences the volunteer's output.

If you want to try this experiment yourself, clone the repository for yourself. Then all you have to do is either overwrite the `TODO: FILE NAME` file or add a file with your own data and change the file read `TODO: EXPLAIN WHERE TO CHANGE FILE READ VARIABLE`. If you add your own data file, make sure it follows the same formatting `TODO: SHOW PROPER FORMATTING HERE`! 
