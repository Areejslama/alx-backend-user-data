#!/usr/bin/env python3
"""this script define class"""
import uuid
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """define class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a given user_id."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """define method"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user = self.user_id_by_session_id.get(session_id)
        return user

    def current_user(self, request=None):
        """define method"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """define method"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        session_id = self.user_id_for_session_id(session_cookie)
        if session_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
