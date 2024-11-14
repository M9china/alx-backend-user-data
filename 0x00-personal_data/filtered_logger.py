#!/usr/bin/env python3
"""Filtering module
"""
import re


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(r'(?<={}=).*?(?={})'.format(
        fields[0], separator), redaction, message)
