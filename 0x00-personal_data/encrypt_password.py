#!/usr/bin/env python3
"""
    The encryption of a password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """It expects to receive one string's argument name of
    the password and then it returns a salted, hashed
    password, to which is then a byte's string.

    Args:
        password (str): the password to be encrypted

    Returns:
        bytes: type of encryption password
    """
    if password:
        return bcrypt.hashpw(str.encode(password),
                bcrypt.gensalt())
