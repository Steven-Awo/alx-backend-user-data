#!/usr/bin/env python3
""" Setting up the session Authentication's module """
from api.v1.auth.auth import Auth

import uuid

class SessionAuth(Auth):
    """ Creating a sessionAuth's class that just inherits
    from the Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creating the session's ID thats for the user_id"""
        if isinstance(user_id, str):
            sessioning_id = str(uuid.uuid4())

            SessionAuth.user_id_by_session_id[sessioning_id] = user_id

            return sessioning_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ the session's id """
        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returning a User's instance thats based on what is
        the cookie value
        """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request)))
