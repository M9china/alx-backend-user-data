#!/usr/bin/env python3
"""A class that inherits from Auth"""

from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Returns base64 part of the authorization header
    for Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization
          header for Basic Authentication"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return base64_authorization_header.encode('utf-8').decode('base64')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str) or \
                user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User()
            user.email = user_email
            user.password = user_pwd
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_auth_header)
        if user_credentials is None:
            return None
        return self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
