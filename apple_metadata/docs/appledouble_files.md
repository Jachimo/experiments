# AppleDouble File 
==================

## Format Internals

Definitive (perhaps) text is "A/UX Toolbox: Macintosh ROM Interface manual",
Chapter 6: 'File Systems and File Formats', pages 6-16 to 6-19.

HTML:
https://web.archive.org/web/20160304101440/http://kaiser-edv.de/documents/Applesingle_AppleDouble_v1.html

PDF:
https://web.archive.org/web/20160325000219/http://kaiser-edv.de/documents/AppleSingle_AppleDouble_v1.pdf


## Header
---------

> The AppleDouble header file has the same format as an AppleSingle file, except that it contains no data fork entry.   
> The magic number for an AppleDouble header file is 0x00051607.   
> The entries in the header file can appear in any order.    
> The header consists of several fixed fields and a list of entry descriptors, each pointing to an entry.

### Header Fields

The header starts with 26 bytes for the magic number, version, "home file system",
and "number of entries" fields.

* Magic number:        4 B
* Version number:      4 B
* Home file system:   16 B (ASCII)
* Number of entries:   2 B

Then it goes to a list of zero or more fixed-length, 12 byte records.
The number of records in the list is specified earlier in the header.

* Entry #1 - ID:       4 B
* Entry #1 - Offset:   4 B 
* Entry #1 - Length:   4 B
* Entry #2 - ID:       4 B
* Entry #2 - Offset:   4 B 
* Entry #2 - Length:   4 B
* _Repeat as many times as header specifies_
* Entry #N - ID:       4 B
* Entry #N - Offset:   4 B 
* Entry #N - Length:   4 B

After this list ends, the file becomes data sections: the actual data specified by
the offset/length values for each Entry with a specified ID.

> Byte ordering in the file-header fields follows MC68000 [...] conventions.

This means "big endian" format, here in 2025.
Also, M68K had a 16b / 2B word length.   
See https://www.cs.utoronto.ca/~sengels/csc258/lectures/M68k_4up.pdf

* AppleSingle Magic number: `0x00051600`
* Version number in original "A/UX Toolbox" book: `0x00010000`
* Home file system is encoded in ASCII, "padded with spaces" and left-adjusted (?) in the column
* Number of entries is an unsigned 16b, big-endian integer, if "other than 0, then that number of entry descriptors immediately follows."
* Each Entry (group of 3 fields) is 12 B, header is 26 B total; file must be len(n) = 26 + (12 * n)


### Entry ID Field (4 bytes)

Value of the Entry ID is important for further parsing.

> The field holds an unsigned, 32-bit number.
> Apple Computer has defined a set of entry IDs and their values.

From https://formats.kaitai.io/apple_single_double/python.html
Can also be found (formatted differently) in Kazakov C++ parser source

data_fork = 1
resource_fork = 2
real_name = 3
comment = 4
icon_bw = 5
icon_color = 6
file_info = 7   #(see note)
file_dates_info = 8
finder_info = 9
macintosh_file_info = 10
prodos_file_info = 11
msdos_file_info = 12
afp_short_name = 13
afp_file_info = 14
afp_directory_id = 15

All entry IDs from 0 to 0x7FFFFFFF are reserved to Apple.

> The rest of the range is available for other definitions.   
> The entry data follows all of the entry descriptors.   
> The data in each entry must be in a single, contiguous block.   
> You can leave holes in the file for later expansion.   

> Put the entries that are most often read, such as "Finder info," as close as possible to the header,
> to increase the probablity that a read of the first block or two will retrieve these entries.

> [In an AppleDouble header file,] put the resource fork at the end of the file because the resource fork is the entry most likely to expand.

Samba on the Buffalo TeraStation (and probably Samba generally) seems to be consistent in this,
it looks like the resource fork item is always last in the header file.


### Offset/Length (4 bytes each)

> This field contains an unsigned 32-bit number 
> that shows the offset of the beginning of the entry's data 
> from the beginning of the file.

Note that the offset is from the **beginning of the file**,
not the beginning of the entry data section of the file.  

There are no delimiters in the data section.

N.B.: seek(0) before first seek(offset) or you will misread


## Entries
----------

### file_info (7) entries

The content of a file_info (7) data object are obtained by seek()ing
to the offset associated with the entry, then read()ing it in some way
for the specified length.

Paraphrasing from A/UX book:

> For Macintosh HFS files, the entry is 16 B long and consists of
> three long-integer dates (create date, modification date, last backup date)
> and a long integer containing 32 Boolean flags.

Flags:

> Where 0 is the least-significant bit and 31 is the most-significant bit,
> bit 0 of the Macintosh "file info" entry is the Locked bit, and 
> bit 1 is the Protected bit.

There is a visual in the book of an 8x4 grid, with the two last cells in the bottom row
marked 'Protected' and 'Locked':

    0000 0000
    0000 0000
    0000 0000
    0000 00PL


### finder_info (9) entries

> The 'Finder info' entry consists of 16 bytes of Finder information followed by 16
> bytes of extended Finder information (the fields `ioFlFndrInfo` followed by 
> `ioFlXFndrInfo`, as returned by the `PBGetCatinfo` call). These fields contain
> extended-file-attribute information.  See _Inside Macintosh_, Volume VI, for a 
> description of the subfields in these fields. 
> Newly created files contain zeros in all 'Finder info' fields.

The 'Finder info' element is where we can find the first trace of Finder color labels
that have been set on the originating HFS/HFS+ filesystem.

* `ioFlFndrInfo` - "Desired Finder information" or "Mask for Finder information"
  depending on `ioSearchInfo1` vs. `ioSearchInfo2`; probably safer to use the 
  later / more recent definition.
    * From [GetCatInfo][]: "ioFlFndrInfo is a record of type "FInfo," 
      and contains 16 bytes of "Finder Information" about the file."
    * Begins with `fdType` which is 4 byte file type
    * Then `fdCreator` which is a 4 byte "creator signature"
    * And then `fdFlags`, 2 bytes (16 bits) of mostly-one-bit flags with meanings:
        * Bit 0: Reserved
        * Bits 1-3: Color coding; a value from 0-7 indicating Finder color and Label
        * Bits 4-5: Reserved
        * Bit 6: `isShared` flag
        * Bit 7: `hasNoINITs` flag
        * Bit 8: `hasBeenInited` flag
        * Bit 9: Reserved
        * Bit 10: `hasCustomIcon` flag
        * Bit 11: `isStationery` flag
        * Bit 12: `nameLocked` flag
        * Bit 13: `hasBundle` flag
        * Bit 14: `isInvisible` flag
        * Bit 15: `isAlias` flag

* `ioFlXFndrInfo` - "Desired extended Finder information" or "Mask for Finder information"
    * Have not seen any files on SMB share that have this filled with anything other than zeros

[GetCatInfo]: https://rbrown.incolor.com/tutorials/getcatinfo.htm
