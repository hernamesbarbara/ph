#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""ph.py
"""
from __future__ import print_function
import sys
import os
import json
from phonenumbers import normalize_digits_only, is_valid_number_for_region
from phonenumbers import parse as parse_number
from phonenumbers import country_code_for_region, region_code_for_country_code
import re

COUNTRY_RG = re.compile(r"^(\+\d+)(.*)")

def rm_punct_leaving_plus_sign(num):
    prefix, num = COUNTRY_RG.match(num).groups()
    num = normalize_digits_only(num)
    return '{} {}'.format(prefix, num)

def parse_phone(phone_str, country_code=0, alpha2=u"US"):
    "returns a dict with phone number properties if the string is parsable"
    """
        returns dict w/: phone_str, phone_str_digits_only, country_code, region, errors (if any)
    """
    try:
        if COUNTRY_RG.match(phone_str):
            phone = parse_number(rm_punct_leaving_plus_sign(phone_str), keep_raw_input=True)
        elif country_code != 0:
            phone = parse_number(u"+{} {}".format(country_code, phone_str), keep_raw_input=True)
        else:
            country_code = country_code_for_region(alpha2)
            if country_code != 0:
                phone = parse_number(u"+{} {}".format(country_code, phone_str), keep_raw_input=True)
            else:
                phone = parse_number(phone_str, alpha2, keep_raw_input=True)
        phone_dict = phone.__dict__.copy()
        phone_dict['region_code'] = region_code_for_country_code(phone.country_code)
        phone_dict['phone_str'] = phone_str
        phone_dict['is_valid_for_region'] = is_valid_number_for_region(phone, region_code_for_country_code(phone.country_code))
    except:
        keys = ['region_code','italian_leading_zero','extension','national_number','is_valid_for_region','raw_input','country_code_source','phone_str','country_code','number_of_leading_zeros','preferred_domestic_carrier_code']
        phone_dict = {k: None for k in keys}
        phone_dict['phone_str'] = phone_str
    return phone_dict
