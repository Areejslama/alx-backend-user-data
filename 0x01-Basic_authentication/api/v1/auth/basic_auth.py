#!/usr/bin/env python3
"""this script to define class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """define class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """define method"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
