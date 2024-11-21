#!/usr/bin/env python3
"""hash password module"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth():
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Takes in a password string arguments and returns a salted, hashed
        password, which is a byte string."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Takes in password and email and returns user"""
        existing_user = None
        try:
            existing_user = self._db.find_user_by(email=email)
        except Exception:
            pass
        if existing_user:
            raise ValueError(f'User {email} already exists')

        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided password is valid"""
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True

        except Exception:
            pass
        return False

    def _generate_uuid(self) -> str:
        """Generate a UUID"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        except Exception:
            raise ValueError('seesion not created')

        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
