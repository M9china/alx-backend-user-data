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
        """Create a new session for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get user from session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
            self._db.update_user(user.id, reset_token=None)
        except Exception:
            raise ValueError
