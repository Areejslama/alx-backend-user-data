#!/usr/bin/env python3
"""this script to encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """define function"""
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """define function"""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

