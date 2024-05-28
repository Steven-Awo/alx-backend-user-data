#!/usr/bin/env python3
"""
Creating the auth's module
"""
from bcrypt import hashpw, gensalt

from db import DB

from user import User

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Creating the hash for a password to pass for
    the user

    Args:
        password (str): this is the password of the user

    Returns:
        str: password hashed
    """
    return hashpw(password.encode('utf-8'), gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This is to register a new user privately

        Args:
            email (str): this is the user's email
            password (str): this is the user's password

        Returns:
            User: the user tht was just registered
        """
        try:
            self._db.find_user_by(email=email)

            raise ValueError(f"User {email} already exists")

        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
