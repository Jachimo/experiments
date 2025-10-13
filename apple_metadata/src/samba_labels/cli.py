"""Main application entry point."""

import sys
from samba_labels import __version__
from samba_labels.processor import AppleDoubleMetadata

def dump_file(args=sys.argv) -> int:
    """Dump contents of AppleDouble file"""

    if len(args) == 2:
        inpath = args[1]
    else:
        print("Wrong number of arguments")
        return 1
    
    adm = AppleDoubleMetadata(inpath)
    print(adm.dump())

    return 0
