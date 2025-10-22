# Apple-to-Linux "Labels" Converter for SMB Shares

Tools for working with Mac OS X's Finder "Labels", as stored on SMB
shares using invisible AppleDouble sidecar files.

The primary goal is to parse the sidecar files so the Labels can be
retrieved and written to the files in a more cross-platform, accessible way.


## Configuration

The project uses Poetry for dependency management. 
Project configuration is in `pyproject.toml`.


## Sample Usage

For the impatient looking for a tl;dr:

    cd path/to/this/project
    poetry install
    cd path/to/files/with/metadata
    
    # Run on files of interest using a Bash-style for loop:
    for f in *.ext; do 
        set_color_sidecar "$f"
    done

It's probably a good idea to run it on a handful of files first, for testing.


## Command Reference

Install all dependencies into the local environment:

   poetry install

This is necessary before running any of the commands below.


### Dump

Dump the AppleDouble metadata for a single file in human-readable format:

   poetry run dump_file /mnt/myshare/path/to/file

Note that the single argument is the path towards a *visible* file on the SMB share
or filesystem; the utility will add the leading `._` to find the related AppleDouble
file automatically.


### Print Finder Color

Print the Finder 'Label' color for a single file:

    poetry run print_finder_color /mnt/myshare/path/to/file

This prints the default color associated with the numeric (1-7) flag set in the
AppleDouble sidecar file.  (Files without a color set have the flag = 0.)


### Set Color in Linux xattr

Extract the Finder 'Label' color and write it to the Linux extended attribute
`user.color` in the filesystem.

    poetry run set_color_xattr /mnt/myshare/path/to/file

Note that this *will not work* unless the underlying filesystem supports
extended attributes.  If the target file is on a SMB share, this requires xattr
support to be enabled in the server/share configuration.  Most NAS devices
do not seem to enable this by default, and if you are seeing AppleDouble files
being created by Mac OS X, it's a pretty good indication it's not enabled.

To realistically use this command, you should probably copy the files of interest
**along with their AppleDouble metadata files** to a real disk-backed filesystem
like EXT4, XFS, ZFS, etc.


### Set Color in XSD Metadata Sidecar File

Extract the Finder 'Label' color and write it to the DigiKam 'Color' field in
an XSD (XML RDF) metadata sidecar file, which will be created if it doesn't
already exist.

The attribute written is `XMP-digiKam:ColorLabel` and it takes an integer value
from 1-9 which corresponds to colors in DigiKam as shown in the Enum `DigikamColors`
in `utility.py`.

    poetry run set_color_sidecar /mnt/myshare/path/to/file

Note that the XSD sidecar file will be created by adding `.xsd` to the entire input
filename including its extension.  So e.g. "bigbear.tif" will have a sidecar file
named "bigbear.tif.xsd" created.  This is the naming schema that DigiKam expects.

Also note that ExifTool is used with the `-overwrite_original` to prevent creation
of `_original` files everywhere, which can be slow on remote SMB shares.
Use with appropriate caution if you already have XSD sidecar files, since there's
no guarantee that ExifTool won't mangle them (although it probably won't).
