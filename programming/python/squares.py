#!/usr/bin/env python

import sys

def squares():
    # Prompt users for a number and a number of iterations
    #  Then construct a list of squares of that number.
    
    a = int(raw_input("Enter an integer: "))
    max = int(raw_input("Enter number of iterations: "))

    L = []
    i = 1
    while i < max:
        L.append(a**i)
        i = i+1

    return L

# For test purposes, print it:
for item in squares():
    print item

