#!/usr/bin/env python3
"""A class that manages an API authentication"""

from flask import request
import os
from typing import List, TypeVar
import re


class Auth:
    """A class to manage an API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function that returns true if not a path, if excluded_paths
        is None and returns false if path is excluded_paths"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """A function that checks for authorization"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that returns None"""
        return None
