#!/usr/bin/python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'exif-revgeo',
    version = '0.1.0',
    description = 'This utility reads the GPS coordinates from your photos, reverse geocode them, and write the result to the appropriate EXIF city/country location tags.',
    long_description = long_description,
    url = 'https://github.com/fg1/exif-revgeo',
    author = 'fg1',
    license = 'BSD',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
    ],

    keywords = 'exif reverse-geocoding',
    packages = find_packages(),
    install_requires = ['requests'],

    entry_points = {
        'console_scripts': [
            'exif_revgeo=exif_revgeo:cli',
        ],
    },
)
