#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """Add a user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find user by arbitrary keyword arguments"""
        if not kwargs:
            raise InvalidRequestError('No arguments for filtering.')

        try:
            user = self.__session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound('No user found matching the criteria.')
            return user
        except AttributeError as e:
            raise InvalidRequestError('Invalid query arguments.') from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """update existing user"""
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f'{key} is not a valid attribute for user')
            setattr(value, key, user)
        self.__session.commit()
