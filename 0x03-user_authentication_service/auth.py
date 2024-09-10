#!/usr/bin/env python3
"""this script define bycrypt"""
import bcrypt



def _hash_password(password: str) -> bytes:
    """define method"""
    encoded_password = password.encoding('utf-8')

    hashed_password = bcrypt.hashpw(encoded_password, nsalted=True
