#!/usr/bin/env python3
"""this script to add an expiration date to a Session ID"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """define a class"""
    def __init__(self):
        """init method"""
        try:
            duration = int(getenv("SESSION_DURATION"))
        except Exception:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None):
        """define function"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None
        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """define function"""
        if session_id is None:
            return None

        user_info = self.user_id_by_session_id.get(session_id)
        if user_info is None:
            return None

        if self.session_duration <= 0:
            return user_info.get("user_id")
        created_at = user_info.get("created_at")
        if created_at is None:
            return None

        expire = created_at + timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return None

        return user_info.get("user_id")
