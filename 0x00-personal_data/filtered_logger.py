#!/usr/bin/env python3
"""
    The setting up of the RedactingFormatter
"""

import re

from typing import List

import logging

import csv

import mysql.connector

import os

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
    """ The returning of the log message's that were
    obfuscated

    Args:
        fields: a list of strings representing all fields
        to obfuscate
        redaction: a string representing by what the
        field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)
    """
    return re.sub(
            r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)",
            lambda match: match.group(1) + "=" + redaction
            if match.group(1) in fields else match.group(0), message)

def get_logger() -> logging.Logger:
    """By returning a logger's object """
    lgn = logging.getLogger("user_data")

    lgn.setLevel(logging.INFO)

    lgn.propagate = False

    shlr = logging.StreamHandler()

    shlr.setFormatter(RedactingFormatter(PII_FIELDS))

    lgn.addHandler(shlr)
    return lgn

def get_db() -> mysql.connector.connection.MySQLConnection:
    """We are connecting to the MySQL's database """
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "localhost"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "root"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )

def main():
    """
    Creating the main function
    """
    connt = get_db()
    userrs = connt.cursor()
    userrs.execute("SELECT CONCAT('name=', name, ';ssn=', ssn, ';ip=', ip, \
        ';user_agent', user_agent, ';') AS message FROM users;")
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()

    for userr in userrs:
        logger.log(logging.INFO, userr[0])


if __name__ == "__main__":
    main()
