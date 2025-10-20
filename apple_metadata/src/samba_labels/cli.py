"""Main application entry point."""

import sys
import os
import logging
from samba_labels import __version__
from samba_labels.processor import AppleDoubleMetadata

def dump_file(args=sys.argv, loglev=logging.DEBUG) -> None:
    """ Dump contents of AppleDouble file """
    if len(args) != 2: 
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath = args[1]
    
    md = AppleDoubleMetadata(inpath, loglev)
    print(md.dump())


def print_finder_color(args=sys.argv, loglev=logging.WARNING) -> None:
    """ Print the decimal representation of the 3-bit Label flags """
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    md: AppleDoubleMetadata = AppleDoubleMetadata(inpath, loglev)
    try:
        print(f"{inpath.split(os.path.sep)[-1]}: {md.color.name}")
    except:
        raise ValueError(f"Couldn't read Finder color flags in {inpath}")
        

def parse_with_kaitai(args=sys.argv) -> None:
    """ Use the Kaitai-generated Python library to parse an AppleDouble file. """
    raise NotImplementedError("Kaitai not implemented yet")
    