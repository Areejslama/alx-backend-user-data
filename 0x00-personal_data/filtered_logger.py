#!/usr/bin/env python3
"""
This script defines a function to obfuscate sensitive data"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates sensitive fields"""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)

    return message
