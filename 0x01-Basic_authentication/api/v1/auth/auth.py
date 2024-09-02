#!/usr/bin/env python3
"""define auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """define class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return require auth"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        path = path.rstrip('/')
        for excluded_paths in excluded_paths:
            if  excluded_paths.rstrip('/') == path:
                return False
            return True

    def authorization_header(self, request=None) -> str:
        """define header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """define user"""
        return None
