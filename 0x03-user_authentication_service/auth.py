#!/usr/bin/env python3
"""define method"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """define function"""
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """define method"""
    new_uuid = str(uuid.uuid4())
    return new_uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """define method"""
        try:
            new_user = self._db.find_user_by(email=email)
            password_bytes = password.encode('utf-8')
            if bcrypt.checkpw(password_bytes, new_user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """to create session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id,  session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """define method"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user is None:
                return None
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """define method"""
        try:
            user = self._db.update_user(user_id=user_id, session_id=None)
            if user is None:
                return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """define function"""
        reset_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """define method"""
        hashed =  _hash_password(password)
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                    user.id, hashed_password=hashed, reset_token=None
                )
        except NoResultFound:
            raise ValueError
