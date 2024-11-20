#!/usr/bin/env python3
"""hash password module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import IntegrityError


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
