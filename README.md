exif-revgeo: Reverse geocode your photos
========================================

This utility reads the GPS coordinates from your photos, reverse geocode them, and write the result to the appropriate EXIF city/country location tags.

## Installation

This script is based on [exiftool](http://owl.phy.queensu.ca/~phil/exiftool/) for the EXIF operations and [mugiss](https://github.com/fg1/mugiss) for the reverse geocoding.

Once both tools are installed, simply clone the repository:
```
$ pip install --upgrade https://github.com/fg1/exif-revgeo/archive/master.tar.gz
```

## Usage

```
usage: exif-revgeo [-h] [--exiftool-bin EXIFTOOL_BIN] [--rd-args RD_ARGS]
                   [--wr-args WR_ARGS] [-o] [-d]
                   path

Add city and country in EXIF based on GPS coords

positional arguments:
  path                  files or folder to process

optional arguments:
  -h, --help            show this help message and exit
  --exiftool-bin EXIFTOOL_BIN
                        exiftool binary to use
  --rd-args RD_ARGS     exiftool read arguments
  --wr-args WR_ARGS     exiftool write arguments
  -o, --overwrite-tags  Overwrite existing tag values
  -d, --dry-run         Do not perform any file modification
```

Examples:

```bash
# Apply on all the jpg files in the current directory:
$ ./exif-revgeo.py *.jpg

# Apply on all the image files of a given directory:
$ ./exif-revgeo.py ~/Pictures/2015/10

# Apply recursively on all the image files contained in a directory:
$ ./exif-revgeo.py --rd-args='-r' ~/Pictures
```

