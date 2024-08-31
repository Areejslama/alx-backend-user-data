#!/usr/bin/env python3
"""
This script defines a function to obfuscate sensitive data"""
import re
from typing import List, Tuple
import logging
import mysql.connector
import os


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates sensitive fields"""
    for field in fields:
        pattern = rf'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)

    return message


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """define function"""
        log = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """define function"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.MySQLConnection:
    """define function"""
    mydb = mysql.connector.connect(
            username=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', 'root'),
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
            )
    return mydb
