#!/usr/bin/env python3
"""this script to define class"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """define class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """define method"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """define method"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string

        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """define method"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user, password = decoded_base64_authorization_header.split(':', 1)
        return user, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """define method"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if users and users[0].is_valid_password(user_pwd):
            return users[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """define method"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = (
                self.extract_base64_authorization_header(auth_header)
            )
        if base64_auth_header is None:
            return None

        decoded_auth_header = (
                self.decode_base64_authorization_header(base64_auth_header)
            )
        if decoded_auth_header is None:
            return None

        credentials = self.extract_user_credentials(decoded_auth_header)
        if credentials is None:
            return None

        user_email, user_pwd = credentials
        return self.user_object_from_credentials(user_email, user_pwd)
