#!/usr/bin/env python3
"""
BD class
"""

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Created to add user to the database

        Args:
            email (string): taking in the email for user
            hashed_password (string): the password just for user
        Returns:
            User: the user just created
        """
        if not email or not hashed_password:
            return
        userr = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(userr)
        session.commit()
        return userr
