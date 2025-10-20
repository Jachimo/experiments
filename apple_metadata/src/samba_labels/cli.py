"""Main application entry point."""

import sys
import os
import logging
import xattr  # see https://github.com/iustin/pyxattr

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
    # Use get_finder_color() below
    print(f"{inpath.split(os.path.sep)[-1]}: {get_finder_color(inpath, loglev)}")


def get_finder_color(inpath, loglev=logging.WARNING) -> str:
    """ Get the Finder 'Label' color and return it as a string """
    md: AppleDoubleMetadata = AppleDoubleMetadata(inpath, loglev)
    try:
        return md.color.name
    except:
        raise ValueError(f"Couldn't read Finder color flags in {inpath}")


def print_xattrs(args=sys.argv, loglev=logging.DEBUG) -> None:
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    xlist: list = xattr.listxattr(inpath)
    for xa in xlist:
        print(f"{xa.decode('utf-8')} : {xattr.getxattr(inpath, xa).decode('utf-8')}")


def set_color_xattr(args=sys.argv, loglev=logging.DEBUG) -> None:
    """ Sets the extended attribute user.color to the Finder label color from the AppleDouble metadata.
        Note that this depends on the underlying filesystem supporting extended attributes. """
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    md: AppleDoubleMetadata = AppleDoubleMetadata(inpath, loglev)

    xattr.setxattr(inpath, "user.color", md.color.name)


def parse_with_kaitai(args=sys.argv) -> None:
    """ Use the Kaitai-generated Python library to parse an AppleDouble file. """
    raise NotImplementedError("Kaitai not implemented yet")
    