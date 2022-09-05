#!/usr/bin/env python

import sys

data = sys.stdin

print "-> The first line is:"
print data.readline()

print "-> The next 10 lines are:"
i = 0
while i < 10:
    print data.readline()
    i = i + 1 

sys.exit(0)
