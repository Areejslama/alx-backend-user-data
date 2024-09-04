#!/usr/bin/env python3
"""this script define class"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """define class"""
    def __init__(self):
        """Initialize the session storage."""
        self.user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """define method"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
