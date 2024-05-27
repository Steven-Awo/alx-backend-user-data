"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
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

        sessioning = self._session

        sessioning.add(userr)

        sessioning.commit()

        return userr
