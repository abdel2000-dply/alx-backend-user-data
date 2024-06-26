#!/usr/bin/env python3
""" Session expiration authentication module
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from typing import List


class SessionExpAuth(SessionAuth):
    """ Session expiration authentication class
    """
    def __init__(self):
        """ Constructor """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID
        """
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
        """ User ID based on a Session ID """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        user_id = session_dict.get('user_id')

        if self.session_duration <= 0:
            return user_id
        if 'created_at' not in session_dict:
            return None

        created_at = session_dict.get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return user_id
