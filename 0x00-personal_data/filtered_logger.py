#!/usr/bin/env python3
"""Filtering module
"""
import re


def filter_datum(fields, redaction, message, separator):
    return re.sub(rf'({"|".join(re.escape(f)
                                for f in fields)})=.+?{separator}',
                  lambda match: f"{
                      match.group(1)}={redaction}{separator}",
                  message)
