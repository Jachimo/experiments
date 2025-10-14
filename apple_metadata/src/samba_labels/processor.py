# Processing logic for AppleDouble metadata.
#  Ref http://kaiser-edv.de/documents/AppleSingle_AppleDouble.pdf

from operator import truediv
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
import os
import logging

class AppleDoubleMetadata:
    def __init__(self, filepath, log_level=logging.DEBUG):
        # Logging setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.filepath = filepath
        self.appledoublepath = ""
        self.entries = {}
        
        # Modern AppleDouble files usually have "._" prepended to the filename
        #  Older implementations can use "%" or "R." prefixes instead
        self.appledoublepath = os.path.join(
            os.path.dirname(filepath), 
            f"._{os.path.basename(filepath)}")
        
        self.logger.info(f"Checking for AppleDouble file at {self.appledoublepath}")
        if not os.path.exists(self.appledoublepath):
            # TODO: Check for old-style "%filename" and "R.filename" as well
            raise FileNotFoundError(f"AppleDouble file not found: {self.appledoublepath}")
        self.logger.info(f"File found at {self.appledoublepath}")

        with open(self.appledoublepath, "rb") as f:
            stream = KaitaiStream(BytesIO(f.read()))
            self._parse_stream(stream)
    

    def _parse_stream(self, stream):
        self.logger.debug("Starting _parse_stream()")

        self.magic: bytes = stream.read_bytes(4)  # returns bytes
        #self.magic: int = stream.read_u4be()    # returns integer ?
        self.version: int = stream.read_u4be()
        self.reserved: bytes = stream.read_bytes(16)
        self.num_entries: int = stream.read_u2be()

        self.logger.info(f"Found {self.num_entries}")
        self.logger.debug(f"Magic bytes: {self.magic}")

        # Per kaitai.io and ArchiveTeam, apple_double = 00 05 16 07 (decimal 333319)
        if self.magic != b'\x00\x05\x16\x07':
            self.logger.warning(f"Invalid or unusual magic number: {self.magic}")
        
        for _ in range(self.num_entries):
            entry_id: int = stream.read_u4be()   # elsewhere called "type"
            offset: int = stream.read_u4be()     # aka "ofs_body"
            length: int = stream.read_u4be()     # aka "len_body"
            self.entries[entry_id] = {
                "offset": offset,
                "length": length
            }
        
        for eid in self.entries:
            self.logger.debug(f"Reading entry with ID = {eid}")
            stream.seek(0)
            stream.seek(self.entries[eid]["offset"])
            data: bytes = stream.read_bytes(self.entries[eid]["length"])
            self.entries[eid]["obj"]= AppleDoubleMetadata.Entry(eid, data)


    class Entry:
        # this is cribbed from https://formats.kaitai.io/apple_single_double/python.html
        # License is https://spdx.org/licenses/CC0-1.0.html

        class Types(IntEnum):
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
        
        def __init__(self, eid: int, data: bytes, log_level=logging.DEBUG):
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(log_level)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s: %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            
            self.logger.debug(f"Creating Entry instance for ID={eid}")

            # Look up entry type in Types enum and store integer to self.types
            self.type: int = KaitaiStream.resolve_enum(
                AppleDoubleMetadata.Entry.Types, 
                eid
            )

            self.logger.debug(f"  ID corresponds to type {AppleDoubleMetadata.Entry.Types(self.type)}")

            # Special handling for finder_info entries (type 9)
            if self.type == AppleDoubleMetadata.Entry.Types.finder_info:
                self.logger.debug(f"  Finder info entry detected, parsing subfields")
                ds = KaitaiStream(BytesIO(data))
                # Per Apple docs, 16B of 'Finder information' followed by 16B of extended info
                # "the fields ioFlFndrInfo followed by ioFlXFndrInfo, as returned by the PBGetCatinfo call"
                self.file_type = ds.read_bytes(4)
                self.file_creator = ds.read_bytes(4)
                #self.flags = ds.read_u2be()
                self.flags = ds.read_bytes(2)
                self.location = ds.read_bytes(4)
                self.folder_id = ds.read_u2be()
            
            # Special handling for file_info entries (type 7)
            if self.type == AppleDoubleMetadata.Entry.Types.file_info:
                self.logger.debug(f"  File info entry detected, parsing subfields")
                ds = KaitaiStream(BytesIO(data))
                # For Macintosh HFS files, the entry is 16 bytes long and consists of three long-integer dates 
                # (create date, last modification date, and last backup date) 
                # and a long integer containing 32 Boolean flags.
                self.cdate_bytes = ds.read_bytes(4)
                self.mdate_bytes = ds.read_bytes(4)
                self.bdate_bytes = ds.read_bytes(4)
                self.flags_bytes = ds.read_bytes(4)

    def dump(self):
        from pprint import pprint
        """ Dump contents to stdout, mostly for debugging """
        print("---------------------------------")
        print(f"File Path: {self.filepath}")
        print(f"AppleDouble Path: {self.appledoublepath}")
        print(f"Number of Entries: {self.num_entries}")
        print()
        for e in self.entries:
            print(f"  EID: {e}")
            print(f"  Offset {self.entries[e]['offset']} (Length {self.entries[e]['length']}) ")
            #print(self.entries[e]["data"])
            eobj = self.entries[e]["obj"] # Entry object
            pprint(vars(eobj))
            print()
