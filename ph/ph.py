#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""ph.py
"""
from __future__ import print_function
import sys
import os
from phonenumbers.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException
import phonenumbers as pn
from pycountry import countries
import re
import string

COUNTRY_ALPHA2 = u"US"
RG_COUNTRY_CODE   = re.compile(r"^(\+\d+)(.*)")

def find_dialing_code_from_alpha2(alpha2):
    return pn.country_code_for_region(alpha2)

def find_alpha2_from_dialing_code(alpha2):
    return pn.region_code_for_country_code(alpha2)

def find_alpha2_by_country_name(name):
    "lookup 2 char abbrv using a country name (e.g. 'United States' => 'US')"
    name = name.title()
    if not name in countries.indices['name']:
        return {}
    country_obj = countries.get(name=name)
    country = country_obj.__dict__.copy()
    for field in ["_element", "alpha3", "numeric"]:
        del country[field]
    return country

def find_country_name_by(alpha2):
    "look up name of a country using 2 char abbrv (e.g. 'US' => 'United States')"
    alpha2 = alpha2.upper()
    if not alpha2 in countries.indices['alpha2']:
        return {}
    country_obj = countries.get(alpha2=alpha2)
    country = country_obj.__dict__.copy()
    for field in ["_element", "alpha3", "numeric"]:
        del country[field]
    return country

def parse_phone(phone_str):
    "returns a dict with phone number properties if the string is parsable"
    """
        returns dict w/: phone_str, phone_str_digits_only, country_code, region, errors (if any)
    """
    phone_str = u"".join(phone_str.strip().split())
    if not phone_str.startswith("+"):
        intl_dial_code = pn.country_code_for_region(COUNTRY_ALPHA2)
        prefix = u"+"+unicode(intl_dial_code)
        phone_str = prefix + phone_str
    phone_str_digits_only = u"+"+pn.normalize_digits_only(phone_str)
    try:
        phone_obj = pn.parse(phone_str, keep_raw_input=True)
        error = {}
    except NumberParseException, err:
        err_note = "ERROR CALLING:  `parse_phone('{}')`".format(phone_str)
        err.args = err.args + (err_note,)
        error = {'err_type': err.error_type, 'error_args': err.args}
    phone = {
        "phone_str": phone_str,
        "phone_str_digits_only": phone_str_digits_only,
        "country_code": phone_obj.country_code,
        "error": error
    }
    region = pn.region_code_for_country_code(phone_obj.country_code)
    if region == u"ZZ":
        phone['region'] = {}
    else:
        country = find_country_name_by(alpha2=region)
        phone.update(country)
    return phone

def is_valid(num):
    "True iff `num` is parsed successfully and digits match the int'l dial code found"
    """
        is_valid("+1 22 222 222") == False  # b/c it's not valid USA number but has '+1' prefix)
    """
    try:
        if not isinstance(num, PhoneNumber):
            num = pn.parse(num)
        region_code = pn.region_code_for_country_code(num.country_code)
        return pn.is_valid_number_for_region(num, region_code)
    except:
        return False
