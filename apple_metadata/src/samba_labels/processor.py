# Processing logic for AppleDouble metadata.
#  Ref http://kaiser-edv.de/documents/AppleSingle_AppleDouble.pdf

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
import os

class AppleDoubleMetadata:
    def __init__(self, filepath):
        self.filepath = filepath
        self.appledoublepath = ""
        self.entries = {}
        
        # AppleDouble files have "._" prepended to the filename
        self.appledoublepath = os.path.join(
            os.path.dirname(filepath), 
            f"._{os.path.basename(filepath)}")
        if not os.path.exists(self.appledoublepath):
            raise FileNotFoundError(f"AppleDouble file not found: {self.appledoublepath}")

        with open(self.appledoublepath, "rb") as f:
            stream = KaitaiStream(BytesIO(f.read()))
            self._parse_stream(stream)
    

    def _parse_stream(self, stream) -> True:
        self.magic: bytes = stream.read_bytes(4)  # returns bytes
        #self.magic: int = stream.read_u4be()    # returns integer ?
        self.version: int = stream.read_u4be()
        self.reserved: bytes = stream.read_bytes(16)
        self.num_entries: int = stream.read_u2be()

        # Per kaitai.io, apple_single = 333312, apple_double = 333319
        # Per ChatGPT, apple_double = 344064 (do not trust this)
        # My files are all x00 x05 x16 x07 (decimal 344071) as the first 4 bytes...

        #if self.magic != b'\x00\x05\x16\x00':  # integer 344064
        #    raise ValueError("Not a valid AppleDouble file")
        
        for _ in range(self.num_entries):
            entry_id: int = stream.read_u4be()   # elsewhere called "type"
            offset: int = stream.read_u4be()     # aka "ofs_body"
            length: int = stream.read_u4be()     # aka "len_body"
            self.entries[entry_id] = {
                "offset": offset,
                "length": length
            }
        
        for eid in self.entries:
            stream.seek(0)
            stream.seek(self.entries[eid]["offset"])
            data: bytes = stream.read_bytes(self.entries[eid]["length"])
            self.entries[eid]["obj"]= AppleDoubleMetadata.Entry(eid, data)

        return True  # not sure this is good practice, but...


    #class Entry(KaitaiStruct):
    class Entry:
        # this is lifted from https://formats.kaitai.io/apple_single_double/python.html
        # License is https://spdx.org/licenses/CC0-1.0.html

        class Types(IntEnum):
            data_fork = 1
            resource_fork = 2
            real_name = 3
            comment = 4
            icon_bw = 5
            icon_color = 6
            file_dates_info = 8
            finder_info = 9
            macintosh_file_info = 10
            prodos_file_info = 11
            msdos_file_info = 12
            afp_short_name = 13
            afp_file_info = 14
            afp_directory_id = 15
        
        def __init__(self, eid: int, data: bytes):
            self.type = KaitaiStream.resolve_enum(
                AppleDoubleMetadata.Entry.Types, 
                eid
            )

            if self.type == AppleDoubleMetadata.Entry.Types.finder_info:
                ds = KaitaiStream(BytesIO(data))
                self.file_type = ds.read_bytes(4)
                self.file_creator = ds.read_bytes(4)
                self.flags = ds.read_u2be()
                self.location = ds.read_bytes(4)
                self.folder_id = ds.read_u2be()


    def dump(self):
        """ Dump contents to stdout, mostly for debugging """
        print("---------------------------------")
        print(f"File Path: {self.filepath}")
        print(f"AppleDouble Path: {self.appledoublepath}")
        print(f"Number of Entries: {self.num_entries}")
        print()
        for e in self.entries:
            print(f"  Offset {self.entries[e]['offset']} (Length {self.entries[e]['length']}) ")
            print(f"  EID: {e}")
            #print(self.entries[e]["data"])
            Eobj = self.entries[e]["obj"] # Entry object
            print(f"  Entry Type: {Eobj.type}") # ({AppleDoubleMetadata.Entry.Types(Eobj.type)})")
            if Eobj.type == AppleDoubleMetadata.Entry.Types.finder_info:
                print(f"  File Type: {Eobj.file_type}")
                print(f"  Creator: {Eobj.file_creator}")
                print(f"  Flags: {Eobj.flags}")
                print(f"  Location: {Eobj.location}")
                print(f"  Folder ID: {Eobj.folder_id}")
                print()
        print()
