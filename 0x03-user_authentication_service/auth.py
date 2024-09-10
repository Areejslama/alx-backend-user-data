#!/usr/bin/env python3
"""define method"""
import bcrypt
from db import DB
from user import Base, User
from db import find_user_by
from user import User


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
        new_user = self._db.find_user_by(email)
        if new_user:
            raise ValueError("User <user's email> already exists")
        else:
            new_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
        return user
