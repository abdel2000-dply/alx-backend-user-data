#!/usr/bin/env python3
""" SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """ Create a session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User ID based on a Session ID
        """
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """ Destroy a session ID
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.search({'session_id': session_id})
            if user_session:
                user_session[0].delete()
                return True
        return False
