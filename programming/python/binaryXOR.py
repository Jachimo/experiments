#!/usr/bin/env python

# Sample program that works with binary files

import sys
import struct

def main():    
    # Open input and output files (if no output, use stdout)
    try:
        file1 = open(sys.argv[1], "rb")
    except IOError:
        sys.stderr.write("Could not open first input file. Exiting.\n")
        return 1
    try:
        file2 = open(sys.argv[2], "rb")
    except IOError:
        sys.stderr.write("Could not open second input file. Exiting.\n")
        return 1
    if len(sys.argv) < 4:
        outfile = sys.stdout
    else:
        try:
            outfile = open(sys.argv[3], "wb")
        except IOError:
            sys.stderr.write("Could not open specified output file. Exiting.\n")
            return 1

    # Then read through the files, byte by byte, and XOR them:
    while True:
        # Read one byte from the first file
        char1 = file1.read(1)
        if not char1:
            break
        # Read one byte from the second
        char2 = file2.read(1)
        if not char2:
            sys.stderr.write("File 2 ended unexpectedly. Retry with longer file.\n")
            break
        # XOR the two bytes together, using struct to convert str -> binary
        outbyte = struct.unpack('b',char1)[0]^struct.unpack('b',char2)[0]
        # Write the XORed output to a file, converting back to str
        outfile.write( struct.pack('b',outbyte) )

    # Close files, exit without error condition
    file1.close()
    file2.close()
    outfile.close()
    return 0

    
# Run the program when executed, starting from main()    
sys.exit(main())
