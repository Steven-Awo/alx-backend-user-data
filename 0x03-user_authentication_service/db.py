#!/usr/bin/env python3
"""
BD class
"""

from sqlalchemy import create_engine

from sqlalchemy.exc import InvalidRequestError

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
        sessionn = self._session
        sessionn.add(userr)
        sessionn.commit()
        return userr

    def find_user_by(self, **kwargs) -> User:
        """finding the user by using some arguments

        Returns:
            User: either the user found or raise an error
        """
        userr = self._session.query(User).filter_by(**kwargs).first()
        if not userr:
            raise NoResultFound

        return userr

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updating the user in thedatabase

        Args:
            user_id (int): id thats of the user
        """
        userr = self.find_user_by(id=user_id)
        for keyy, vall in kwargs.items():
            if keyy not in DATA:
                raise ValueError
            setattr(userr, keyy, vall)
        self._session.commit()
        return None
