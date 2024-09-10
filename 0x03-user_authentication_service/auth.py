#!/usr/bin/env python3
"""define method"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """define function"""
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register the added user"""
        try:
            new_user = self._db.find_user_by(email=email)
            if new_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
        return user
