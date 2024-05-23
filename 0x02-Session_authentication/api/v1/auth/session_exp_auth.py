#!/usr/bin/env python3
""" Session expiration authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session expiration authentication class
    """
    def __init__(self):
        """ Constructor
        """
        self.session_duration = getenv('SESSION_DURATION', 0)

    def create_session(self, user_id: str = None) -> str:
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID based on a Session ID
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        user_id = self.user_id_by_session_id[session_id].get('user_id')

        if self.session_duration <= 0:
            return user_id
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None

        created_at = self.user_id_by_session_id[session_id].get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return user_id