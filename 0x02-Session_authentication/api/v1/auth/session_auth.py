#!/usr/bin/env python3
""" Session authentication module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import List, TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID
        """
        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID based on a Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroy a session
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_cookie]
        return True
