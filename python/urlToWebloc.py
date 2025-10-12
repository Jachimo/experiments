#!/usr/bin/env python

import sys
import os.path

def urlToWebloc(file):
    """Converts a no-nonsense .url file to Apple's XML-based .webloc format.

    Returns string."""

    inurl = file.readline().strip()  # read first line of URL file

    outstring = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>URL</key>
	<string>%s</string>
</dict>
</plist>""" % inurl

    return outstring


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Invalid number of arguments. Exiting."
        sys.exit(1)
    print "Reading from", sys.argv[1]
    infile = open(sys.argv[1], "rU")
    outpath = os.path.splitext( sys.argv[1] )[0] + ".webloc"
    print "Output is", outpath
    outfile = open(outpath, "w")
    outfile.write(urlToWebloc(infile))  # see above
    outfile.close()
    infile.close()
    sys.exit(0)

    
