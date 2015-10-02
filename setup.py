#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""setup.py
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'parse phone numbers from command line',
    'author': 'Austin Ogilvie',
    'keywords': 'wrapper for phonenumbers (https://github.com/daviddrysdale/python-phonenumbers.git)',
    'author_email': 'a@yhathq.com',
    'version': '0.1',
    'install_requires': ['phonenumbers', 'pycountry'],
    'packages': ['ph'],
    'include_package_data': True,
    'scripts': ['bin/ph'],
    'zip_safe': False,
    'name': 'ph',
    'license': 'MIT'
}

setup(**config)
