#!/usr/bin/env python3
'''encrypt_password module
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hash_password function
    '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''is_valid function
    '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
