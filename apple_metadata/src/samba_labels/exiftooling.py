""" Convenience code for working with ExifTool """

# Note that exiftool binary must be installed and on $PATH

import os
import subprocess
#import exiftool  # currently unused in favor of naked subprocess.run()
import logging
from tribool import Tribool


class ExifToolTarget:
    """ Represents an item (image file, etc.) that exiftool can be used to read/write metadata to/from """

    def __init__(self, filepath: str, ext=".xmp", log_level=logging.ERROR) -> None:
        self.filepath: str = filepath
        self.mdext: str = ext  # Metadata sidecar file extension, usually ".xmp"
        self.mdpath: str = self.filepath + self.mdext
        self.hassidecar: Tribool = Tribool(None)  # Can be True, False, or None (indeterminate)

        # Logging setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Instantiation
        self.logger.debug(f"Checking if sidecar file exists for {self.filepath}")
        self.hassidecar = self.check_sidecar_exists()


    def check_sidecar_exists(self) -> Tribool:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"{self.filepath} not found")
        if not os.path.exists(self.mdpath):
            return Tribool(False)
        if os.path.exists(self.mdpath):
            return Tribool(True)


    def create_sidecar(self) -> bool:
        if self.hassidecar.value is None:
            self.check_sidecar_exists()
        if self.hassidecar.value is True:
            self.logger.debug(f"Found existing sidecar file at {self.mdpath}")
            return True  # my work here is done
        
        # Else create it by calling exiftool via subprocess
        # The -o option will create an XMP if it doesn't exist but error if it does, will not overwrite
        self.logger.debug(f"Creating new sidecar file for {self.filepath}")
        p = subprocess.run(["exiftool", self.filepath, "-o", self.mdpath])
        if p.returncode == 0:
            self.hassidecar = Tribool(True)
            self.logger.debug(f"Sidecar file successfully created at {self.mdpath}")
            return True
        else:
            self.hassidecar = Tribool(None)  # since we do not know for sure what happened...
            raise subprocess.SubprocessError(f"exiftool returned {p.returncode} while creating sidecar for {self.filepath}")


    def write_field_value(self, fieldname: str, value: str) -> bool:
        """ Use exiftool (external) to write value to the metadata property named fieldname.
            The fieldname argument must be a valid exiftool "tag name". """
        if self.hassidecar.value is not True:
            self.create_sidecar()
        
        p = subprocess.run(["exiftool", f'-{fieldname}={value}', self.mdpath])
        if p.returncode == 0:
            self.logger.debug(f"EXIFTOOL: Wrote {fieldname}={value} to {self.mdpath}")
            return True
        else:
            raise subprocess.SubprocessError(f"exiftool returned {p.returncode} while attempting to write {fieldname} to {self.mdpath}")
    