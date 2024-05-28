#!/usr/bin/env python3
"""
Creating the auth's module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """Creating the hash for a password to pass for
    the user

    Args:
        password (str): this is the password of the user

    Returns:
        str: password hashed
    """
    return hashpw(password.encode('utf-8'), gensalt())
