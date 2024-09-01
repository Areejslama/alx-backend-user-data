#!/usr/bin/env python3
"""this script to encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """define function"""
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed
