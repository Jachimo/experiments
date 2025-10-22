""" Reusable utility logic """

from enum import Enum, IntEnum

finder_to_digikam_color = {
    "Gray" : "Gray",
    "Grey" : "Gray",
    "Green" : "Green",
    "Purple" : "Magenta",
    "Blue" : "Blue",
    "Yellow" : "Yellow",
    "Red" : "Red",
    "Orange" : "Orange",
    False : False,
}


# Below classes are currently unused, but extracted here for future use

class FinderColors(IntEnum):
    """ Color values used by Mac OS Finder, by default """
    Gray   =    1
    Green  =    2
    Purple =    3
    Blue   =    4
    Yellow =    5
    Red    =    6
    Orange =    7

class FinderInfoTypes(IntEnum):
    """ Type codes used by the Finder Info entry """
    data_fork = 1
    resource_fork = 2
    real_name = 3
    comment = 4
    icon_bw = 5
    icon_color = 6
    file_info = 7
    file_dates_info = 8
    finder_info = 9
    macintosh_file_info = 10
    prodos_file_info = 11
    msdos_file_info = 12
    afp_short_name = 13
    afp_file_info = 14
    afp_directory_id = 15

class DigikamColors(IntEnum):
    """ Color codes used by DigiKam in its 'digiKam:ColorLabel' tag/property/field """
    Red      =  1
    Orange   =  2
    Yellow   =  3
    Green    =  4
    Blue     =  5
    Magenta  =  6
    Gray     =  7
    Black    =  8
    White    =  9
