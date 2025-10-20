"""Main application entry point."""

import sys
from samba_labels import __version__
from samba_labels.processor import AppleDoubleMetadata

def dump_file(args=sys.argv) -> int:
    """ Dump contents of AppleDouble file """
    if len(args) != 2: 
        raise ValueError("Wrong number of arguments")
    inpath = args[1]
    
    md = AppleDoubleMetadata(inpath)
    print(md.dump())
    
    return 0


def read_finder_color(args=sys.argv) -> int:
    """ Print the decimal representation of the 3-bit Label flags """
    if len(args) != 2:
        raise ValueError("Wrong number of arguments")
    inpath = args[1]

    md = AppleDoubleMetadata(inpath)
    try:
        finderinfo: AppleDoubleMetadata.Entry = md.entries[9]["obj"]
        print(f"Color flags set to: {finderinfo.finder_colorval}")
    except:
        raise ValueError(f"Couldn't read Finder color flags in {inpath}")
        


def parse_with_kaitai(args=sys.argv) -> int:
    """ Use the Kaitai-generated Python library to parse an AppleDouble file. """
    raise NotImplementedError("Kaitai not implemented yet")
    