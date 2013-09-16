#!/usr/bin/env python

# Taken from http://linuxclues.blogspot.com/2009/01/python-calculate-prime-numbers.html

#Prime numbers
import sys
import math

print "Prime numbers"

#Asks user how many numbers he wants to calculate.
top = int(raw_input("How many prime numbers do you want to calculate?: "))

if (top <1 ) :
    print "Error: Invalid number. It must be greater than one"
    sys.exit

#Initializing some variables
a = 3    # first number to test if it is prime.
result = [2]  # result list begins with prime number 2.
num = 1   # number of already calculated primes.
print 2,

while num < top : # main loop
    cont = 0

    # Performs the division test
    while 1 :
        divisor = result[cont]   # we only test with already calculated prime numbers.
        
        (quotient, remainder) = divmod(a,divisor)  # calculates quotient and remainder at the same time.

        if (remainder) :
            if divisor <= quotient :
                cont += 1 
            else:
                result.append(a)
                print a,  # number a is a prime.
                num += 1
                break
        else:
            break   # number a is not a prime

    a += 1   # calculate next number to test.
