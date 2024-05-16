#!/usr/bin/env python3
"""
    Setting up the RedactingFormatter
"""

import re

from typing import List

import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Creating theRedacting Formatter's class
    """

    REDACTION = "***"

    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initializing the class attributes """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Creating the format record's function """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """The returning of the log's message that has
    been obfuscated 

    Args:
        fields: a list of strings representing all fields
        to obfuscate
        redaction: a string representing by what the field
        will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)
    """
    return re.sub(r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)",
                  lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)
