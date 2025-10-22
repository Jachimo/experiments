"""Main application entry point."""

import sys
import os
import logging
import xattr  # see https://github.com/iustin/pyxattr

from samba_labels import __version__
from samba_labels.processor import AppleDoubleMetadata
from samba_labels.exiftooling import ExifToolTarget
from samba_labels.utility import finder_to_digikam_color, DigikamColors


def dump_file(args=sys.argv, loglev=logging.DEBUG) -> int:
    """ Dump contents of AppleDouble file """
    if len(args) != 2: 
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath = args[1]
    
    md = AppleDoubleMetadata(inpath, loglev)
    print(md.dump())
    return 0


def print_finder_color(args=sys.argv, loglev=logging.WARNING) -> int:
    """ Print the decimal representation of the 3-bit Label flags """
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]
    # Use get_finder_color() below
    print(f"{inpath.split(os.path.sep)[-1]}: {get_finder_color(inpath, loglev)}")
    return 0


def get_finder_color(inpath, loglev=logging.WARNING) -> str:
    """ Get the Finder 'Label' color and return it as a string """
    md: AppleDoubleMetadata = AppleDoubleMetadata(inpath, loglev)
    try:
        return md.color.name
    except:
        raise ValueError(f"Couldn't read Finder color flags in {inpath}")


def print_xattrs(args=sys.argv, loglev=logging.DEBUG) -> int:
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    xlist: list = xattr.listxattr(inpath)
    for xa in xlist:
        print(f"{xa.decode('utf-8')} : {xattr.getxattr(inpath, xa).decode('utf-8')}")
    return 0


def set_color_xattr(args=sys.argv, loglev=logging.DEBUG) -> int:
    """ Sets the extended attribute user.color to the Finder label color from the AppleDouble metadata.
        Note that this depends on the underlying filesystem supporting extended attributes. """
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    aamd = AppleDoubleMetadata(inpath, loglev)
    if aamd.color:
        xattr.setxattr(inpath, "user.color", aamd.color.name)
    return 0


def set_color_sidecar(args=sys.argv, loglev=logging.DEBUG) -> int:
    """ Sets the 'XMP-digiKam' metadata attribute to the Finder label color from the AppleDouble metadata.
        This will create an XMP metadata sidecar file, populated from the file internal metadata using exiftool. """
    if len(args) != 2:
        raise ValueError(f"Wrong number of arguments: {args}")
    inpath: str = args[1]

    try:
        aamd = AppleDoubleMetadata(inpath, loglev)
    except Exception as e:
        print(e)
        return 1
    
    if aamd.color:
        dk_color = finder_to_digikam_color[aamd.color.name]  # get corresponding Digikam color for Finder color
        dk_colorval = DigikamColors[dk_color]  # convert to appropriate integer (see utility.py)
        exmd = ExifToolTarget(inpath, log_level=loglev)
        exmd.write_field_value('XMP-digiKam:ColorLabel', dk_colorval)
    return 0
