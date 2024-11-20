#!/usr/bin/env python3
"""hash password module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns a salted, hashed
    password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
