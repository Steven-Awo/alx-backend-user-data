#!/usr/bin/env python3
"""
    Setting up the RedactingFormatter
"""

import re

from typing import List

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
