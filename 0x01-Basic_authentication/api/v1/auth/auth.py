#!/usr/bin/env python3
"""define auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """define class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """define header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """define user"""
        return None
