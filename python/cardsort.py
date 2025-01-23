#!/usr/bin/env python

import sys

debug = sys.stderr

def cardsort(inlist):
    """Sort a list of alphanumeric strings, similar to a card-sorting machine.
    Returns list."""

    maxlen = 0
    for record in inlist:
        if len(record) > maxlen:
            maxlen = len(record)
    debug.write("DEBUG: Max length is " + str(maxlen) + "\n")

    for i in range(0, len(inlist)):
        while len(inlist[i]) < maxlen:
            inlist[i] = inlist[i] + '\0'  # pad short records with NULLs

    debug.write("--- Beginning Sort ---\n")    
    for m in range(1, maxlen+1):  # iterate over characters from R to L
        changesMade = True
        while changesMade == True:
            changesMade = False
            for i in range(0, len(inlist)-1 ):  # iterate through items in list
                debug.write("DEBUG: Char " + str(maxlen-m) + " Item " + str(i) + '\n')
                debug.write(str(inlist) + '\n')
                if stringtoints( inlist[i] )[maxlen-m] > stringtoints( inlist[i+1] )[maxlen-m]:
                    debug.write("DEBUG: Swapping " + inlist[i] + " and " + inlist[i+1] + '\n')
                    tempstring = inlist[i] # If i comes after i+1, swap them
                    inlist[i] = inlist[i+1]
                    inlist[i+1] = tempstring
                    changesMade = True  # if changes made in this pass, do another one
        debug.write("End of sort.\n")
    return inlist

def stringtoints(instring):
    """Converts a string to a list of integers, with a=1, b=2...z=26.
    Returns list."""
    
    outints = []  # output is a list of integers
    
    lookuptab = { 'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,
              'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14,
              'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21,
              'v':22, 'w':23, 'x':24, 'y':25, 'z':26, }
    upperlower = { 'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e', 'F':'f', 'G':'g',
              'H':'h', 'I':'i', 'J':'j', 'K':'k', 'L':'l', 'M':'m', 'N':'n',
              'O':'o', 'P':'p', 'Q':'q', 'R':'r', 'S':'s', 'T':'t', 'U':'u',
              'V':'v', 'W':'w', 'X':'x', 'Y':'y', 'Z':'z', }
    numerals = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    for char in instring:
        if char in lookuptab:
            outints.append( lookuptab[char] )
        if char in upperlower:
            outints.append( lookuptab[ upperlower[char] ] )
        if char in numerals:
            outints.append( int(char) )
        if char == '\0':
            outints.append(0)  # Make NULLs worth zero
        else:
            pass  # This strips whitespace and unknown characters
    return outints
