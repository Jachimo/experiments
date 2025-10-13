# Apple-to-Linux "Labels" Converter for SMB Shares

Tools for working with Mac OS X's Finder "Labels", as stored on SMB
shares using invisible AppleDouble sidecar files.

The primary goal is to parse the sidecar files so the Labels can be
retrieved and written to the files in a more cross-platform, accessible way.

## Configuration

The project uses Poetry for dependency management. All configuration is in `pyproject.toml`:

## Commands

Install all dependencies into the local environment:

   poetry install

Dump the AppleDouble metadata for a single file in human-readable format:

   poetry run dumpmd /mnt/myshare/path/to/file

Note that the single argument is the path towards a *visible* file on the SMB share
or filesystem; the utility will add the leading `._` to find the related AppleDouble
file automatically.
