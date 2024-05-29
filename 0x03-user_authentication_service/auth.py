#!/usr/bin/env python3
"""
Creating the auth's module
"""
from bcrypt import hashpw, gensalt, checkpw

from db import DB

from user import User

from sqlalchemy.orm.exc import NoResultFound

from uuid import uuid4


def _hash_password(password: str) -> str:
    """Creating the hash for a password to pass for
    the user

    Args:
        password (str): this is the password of the user

    Returns:
        str: password hashed
    """
    return hashpw(password.encode('utf-8'), gensalt())

def _generate_uuid() -> str:
    """This help to generate the uuid

    Returns:
        str: print out the representation of just a new UUID
    """
    return str(uuid4())

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

    def valid_login(self, email: str, password: str) -> bool:
        """The validation login foer a user

        Args:
            email (str): the user's email
            password (str): the user's password

        Returns:
            bool: [description]
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Ceated just for a new session thats for  the user

        Args:
            email (str): the user's email

        Returns:
            str: the string's for representation just of the session ID
        """
        try:
            user = self._db.find_user_by(email=email)

            session_id = _generate_uuid()

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """To get the user just from the session id

        Args:
            session_id (str): the session id used for the user

        Returns:
            str: the user's email
        """
        if session_id is None:
            return
        try:
            userr = self._db.find_user_by(session_id=session_id)

            return userr.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Use to destroy the session created

        Args:
            user_id (int): the user's id
        """
        try:
            user = self._db.find_user_by(id=user_id)

            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """USED in getting the reset password's token

        Args:
            email (str): the user's email

        Raises:
            ValueError: if the user isn't found

        Returns:
            str: the reset's token
        """
        try:
            user = self._db.find_user_by(email=email)

            reset_token = _generate_uuid()

            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update password

        Args:
            reset_token (str): reset token
            password (str): user password

        Raises:
            ValueError: if not found user
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
