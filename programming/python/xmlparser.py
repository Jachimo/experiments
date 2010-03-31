#!/usr/bin/env python

# A sample XML parser, written in Python.
#  Written for Python 2.6.

from xml.dom import minidom

# Try to open the input file
infile = open(sys.argv[1])

# Parse it with minidom
xmldocument = minidom.parse(infile)

# Close the input file
infile.close()

