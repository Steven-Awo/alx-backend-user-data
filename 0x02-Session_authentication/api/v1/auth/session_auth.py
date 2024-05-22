#!/usr/bin/env python3
""" Setting up the session Authentication's module """
from api.v1.auth.auth import Auth

class SessionAuth(Auth):
    """ Creating a sessionAuth's class that just inherits
    from the Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a Session ID for a user_id """
        if isinstance(user_id, str):
            sessioning_id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[sessioning_id] = user_id
            return sessioning_id
