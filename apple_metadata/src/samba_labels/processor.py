# Processing logic for AppleDouble metadata.
#  Ref http://kaiser-edv.de/documents/AppleSingle_AppleDouble.pdf

from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
import os
import logging


class AppleDoubleMetadata:
    def __init__(self, filepath, log_level=logging.WARNING):
        self.filepath: str = filepath
        self.appledoublepath: str = ""
        self.entries: dict = {}
        self.color: str = ""
        self.magic: bytes = bytes(0)
        self.version: int = 0
        self.reserved: bytes = bytes(0)
        self.num_entries: int = 0

        # Logging setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Check for input file
        self.logger.info(f"Processing input data file {self.filepath}")
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Input file not found: {self.filepath}")
        
        # Check for AppleDouble metadata sidecar file:
        #   Modern AppleDouble files usually have "._" prepended to the filename
        #   Older implementations can use "%" or "R." prefixes instead
        self.appledoublepath = os.path.join(os.path.dirname(self.filepath), f"._{os.path.basename(self.filepath)}")
        
        self.logger.debug(f"Checking for AppleDouble file at {self.appledoublepath}")
        if not os.path.exists(self.appledoublepath):
            # TODO: Check for old-style "%filename" and "R.filename" as well
            raise FileNotFoundError(f"AppleDouble file not found: {self.appledoublepath}")
        self.logger.info(f"AppleDouble file found at {self.appledoublepath}")

        with open(self.appledoublepath, "rb") as f:
            stream = KaitaiStream(BytesIO(f.read()))
            self._parse_stream(stream)
    

    def _parse_stream(self, stream):
        self.logger.debug("Starting _parse_stream(): li.52")

        self.magic: bytes = stream.read_bytes(4)  # returns bytes
        self.version: int = stream.read_u4be()
        self.reserved: bytes = stream.read_bytes(16)
        self.num_entries: int = stream.read_u2be()

        self.logger.debug(f"Magic bytes: {hex(int.from_bytes(self.magic, byteorder='big'))}")
        self.logger.debug(f"AppleDouble version {self.version}")
        self.logger.debug(f"Found {self.num_entries} Entry objects")

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
            # Create an Entry object for each, passing self as parent
            self.entries[eid]["obj"]= AppleDoubleMetadata.Entry(self, eid, data, log_level=self.logger.level)


    class Entry:
        def __init__(self, parent, eid: int, data: bytes, log_level=logging.WARNING):
            self.parent = parent  # so we can access parent attributes
            self.type: int = 0
            self.file_type: bytes = bytes(0)
            self.file_creator: bytes = bytes(0)
            self.flags: bytes = bytes(0)
            self.location: bytes = bytes(0)
            self.folder_id: int = 0
            self.finder_colorval: int = 0

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(log_level)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s: %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            
            self.logger.debug(f"Parsing Entry with ID = {eid}")

            # Look up entry type in Types enum and store integer to self.types
            self.type = KaitaiStream.resolve_enum(AppleDoubleMetadata.Entry.Types, eid)
            self.logger.debug(f"  ID corresponds to type {AppleDoubleMetadata.Entry.Types(self.type).name}")

            # Special handling for finder_info entries (type 9) which store the Label color
            if self.type == AppleDoubleMetadata.Entry.Types.finder_info:
                self.logger.debug(f"  Finder info entry detected, parsing subfields")
                ds = KaitaiStream(BytesIO(data))
                # Per Apple docs, 16B of 'Finder information' followed by 16B of extended info
                # "the fields ioFlFndrInfo followed by ioFlXFndrInfo, as returned by the PBGetCatinfo call"
                self.file_type: bytes = ds.read_bytes(4)
                self.file_creator: bytes = ds.read_bytes(4)
                self.flags: bytes = ds.read_bytes(2)  # 16 bits of flags
                self.location: bytes = ds.read_bytes(4)
                self.folder_id: int = ds.read_u2be()
                flagint: int = int.from_bytes(self.flags, byteorder='big')

                self.logger.debug(f"  self.flags = {flagint:b} (Boolean {bool(flagint)}) ")

                if flagint:  # False if all zeros...
                    # Need to extract 3 bits from 16 total, in positions 'Y':  NNNNNNNNNNNNYYYN
                    # This requires some bitwise twiddling...
                    start_mask: int = 1  # counting from LSB, i.e. "right to left"
                    end_mask: int = 4
                    labelmask = ( (1 << (end_mask - start_mask)) - 1) << start_mask
                    colorbits = (flagint & labelmask) >> start_mask

                    self.logger.debug(f"  Flag bits {flagint:b} with bitmask {labelmask:b} -> {colorbits:b} (decimal {colorbits})")
                    
                    self.finder_colorval = colorbits
                    parent.color = AppleDoubleMetadata.Entry.Colors(colorbits)

            
            # Special handling for file_info entries (type 7)
            #  On Buffalo Terastation SMB implementation, these seem to be all zero-byte filled
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
            
            # Type codes above 15 are not defined by Apple (that I can find), unlikely to be valid
            if self.type > 15:
                self.logger.warning(f"Unknown Entry type with value {self.type} found")


        class Types(IntEnum):
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
        
        class Colors(IntEnum):
            """ Color values used by Mac OS Finder, by default """
            Gray   =    1
            Green  =    2
            Purple =    3
            Blue   =    4
            Yellow =    5
            Red    =    6
            Orange =    7


    def dump(self):
        """ Dump contents to stdout, mostly for debugging """
        from pprint import pprint
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
