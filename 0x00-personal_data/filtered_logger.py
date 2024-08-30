#!/usr/bin/env python3
"""this script define function"""
import re


def filter_datum(fields, redaction, message, separator):
    """define function"""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)

    return message
