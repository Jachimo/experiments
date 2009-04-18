#!/usr/bin/env python

"""Test program for working with flat files"""

import sys

INPUT = "inputfile.txt"

def main():
    global INPUT
    print "---> First we go the normal way..."
    print_normal(INPUT)
    print "---> Then we go the reverse..."
    print_reverse(INPUT)

# This function prints all the lines in the inputfile, first to last
def print_normal(inputname):
    infile = open(inputname, 'rU')
    for line in infile:
        print line.rstrip('\n')
    infile.close()

# This function prints all lines, starting with the last one
def print_reverse(inputname):
    infile = open(inputname, 'rU')
    lines = infile.readlines()
    while lines:
        print lines.pop().rstrip('\n')
    infile.close()

main()
