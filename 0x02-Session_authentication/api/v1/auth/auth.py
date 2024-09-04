#!/usr/bin/env python3
"""define auth class"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """define class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return require auth"""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """define header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """define user"""
        return None

    def session_cookie(self, request=None):
        """define method"""
        if request is None:
            return None
        name = getenv('SESSION_NAME')
        return request.cookies.get(name)
