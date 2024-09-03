#!/usr/bin/env python3
"""this script to define class"""
from api.v1.auth.auth import Auth
import base64


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
