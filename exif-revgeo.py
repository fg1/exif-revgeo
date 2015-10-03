#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    exif-revgeo
    ~~~~~~~~~~~

    This utility reads the GPS coordinates from your photos, reverse geocode
    them, and write the result to the appropriate EXIF city/country location
    tags.

    :copyright: (c) 2015 by fg1
    :license: BSD, see LICENSE for more details
"""

from __future__ import print_function
import os
import json
import shlex
import logging
import argparse
import requests
import subprocess

__version__ = "0.1.0"

# IPTC tags used for the location
EXIF_IPTC_LOC = ['City', 'Country-PrimaryLocationName', 'Country-PrimaryLocationCode']

# Description of the webservice doing the reverse geocoding
REVERSE_GEOCODE_URL = 'http://127.0.0.1:8080/rg/%(lat)f/%(lng)f/0.01'
REVERSE_GEOCODE_TRANS = {"city": u"City",
                         "country": u"Country-PrimaryLocationName",
                         "country_iso3166-3": u"Country-PrimaryLocationCode"}

# ----------------------------------------------------------------------------
# Helper functions

logging.basicConfig(format='%(asctime)-15s %(message)s')
log = logging.getLogger('exifloc')

def filter_keys(d, keys):
    """
    Returns dict 'd' with only the keys specified in 'keys'
    """
    return dict((k, v) for k, v in d.iteritems() if k in keys)

def exclude_keys(d, keys):
    """
    Returns dict 'd' without the keys specified in 'keys'
    """
    return dict((k, v) for k, v in d.iteritems() if k not in keys)

# ----------------------------------------------------------------------------
# Reverse geocoding

def reverse_geocode(lat, lng):
    r = requests.get(REVERSE_GEOCODE_URL % {'lat': lat, 'lng': lng})
    if r.status_code != 200:
        return None
    else:
        return json.loads(r.text)

# ----------------------------------------------------------------------------
# EXIF read/write operations

def extract_exif_tags(exiftool_bin, path, rd_args):
    if isinstance(path, basestring):
        path = [path]
    iptc_tags = ['-' + t for t in EXIF_IPTC_LOC]
    data = subprocess.check_output([exiftool_bin] +
                                   shlex.split(rd_args) +
                                   shlex.split('-q -n -j -GPSLatitude -GPSLongitude') +
                                   iptc_tags + path)
    data = json.loads(data)
    return data

def tag_location(exiftool_bin, wr_args, info, overwrite_tags, dry_run):
    rg_loc = reverse_geocode(info['GPSLatitude'], info['GPSLongitude'])
    if rg_loc == None:
        log.warn('Error getting info for %(SourceFile)s (%(GPSLatitude)f, %(GPSLongitude)f)', info)
        return

    # Adapts the returned object to the IPTC names
    for k, v in REVERSE_GEOCODE_TRANS.iteritems():
        rg_loc[v] = rg_loc.pop(k)
    rg_loc = filter_keys(rg_loc, EXIF_IPTC_LOC)

    # Only add tags where they are missing
    if not overwrite_tags:
        exif_loc = filter_keys(info, EXIF_IPTC_LOC)
        rg_loc = exclude_keys(rg_loc, exif_loc.keys())

    if len(rg_loc) == 0:
        return

    # Build exiftool command
    cmd = [exiftool_bin] + shlex.split(wr_args)
    for k, v in rg_loc.iteritems():
        cmd.append('-' + k + "=" + v + "")
    cmd.append(info['SourceFile'])

    # Execute command
    print("> " + ' '.join(cmd))
    if dry_run:
        return
    subprocess.check_call(cmd)

# ----------------------------------------------------------------------------
# Main

def main(args):
    tags = extract_exif_tags(args.exiftool_bin, args.path, args.rd_args)

    # Keeps only the files where the latitude and longitude are set
    tags = [t for t in tags if 'GPSLatitude' in t and 'GPSLongitude' in t]
    for t in tags:
        tag_location(args.exiftool_bin, args.wr_args, t, args.overwrite_tags, args.dry_run)

def cli():
    parser = argparse.ArgumentParser(description='Add city and country in EXIF based on GPS coords')
    parser.add_argument('--exiftool-bin', type=str, help='exiftool binary to use', default='exiftool')
    parser.add_argument('--rd-args', type=str, help='exiftool read arguments', default='')
    parser.add_argument('--wr-args', type=str, help='exiftool write arguments', default='-overwrite_original')
    parser.add_argument('-o', '--overwrite-tags', action='store_true', help='Overwrite existing tag values')
    parser.add_argument('path', type=str, help='files or folder to process')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Do not perform any file modification')
    args = parser.parse_args()

    main(args)

if __name__ == "__main__":
    cli()
