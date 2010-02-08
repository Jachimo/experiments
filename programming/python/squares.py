#!/usr/bin/env python

import sys

def squares(a, stop):
    """Take an integer A and an integer number of iterations S,
    and construct a list of squares A**n, where n is from 1 to S.

    Returns a list."""

    L = []
    i = 1
    while i <= stop:
        L.append(a**i)
        i = i+1

    return L

# For test purposes, work interactively:
if __name__ == "__main__":
    start = int(raw_input("Enter an integer: "))
    iterations = int(raw_input("Enter number of iterations: "))
    for item in squares(start, iterations):
        print item

