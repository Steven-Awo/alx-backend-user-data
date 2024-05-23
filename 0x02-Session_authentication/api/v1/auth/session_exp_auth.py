#!/usr/bin/env python3
"""
Creating the sessionExpAuth's class thats to manage the API's authentication
"""
from api.v1.auth.session_auth import SessionAuth

from datetime import datetime, timedelta

from os import getenv


class SessionExpAuth(SessionAuth):
    """Creating the SessionExpAuth's class for API's authentication
    """

    def __init__(self):
        """Initializing the SessionExpAuth class
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))

        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creating a session for duration
        """
        sessioning_id = super().create_session(user_id)

        if sessioning_id:
            SessionAuth.user_id_by_session_id[sessioning_id] = {
                'user_id': user_id, 'created_at': datetime.now()}

            return sessioning_id

    def user_id_for_session_id(self, sessioning_id=None):
        """Getting the user's ID just from the session
        """
        if not sessioning_id:
            return None
        duration_session_dictry = SessionExpAuth.user_id_by_session_id.get(sessioning_id)

        if not duration_session_dictry:
            return None

        if self.session_duration <= 0:
            return duration_session_dictry['user_id']

        if 'created_at' not in duration_session_dictry:
            return None

        delta = timedelta(seconds=self.session_duration)

        if duration_session_dictry['created_at'] + delta < datetime.now():
            return None

        return duration_session_dictry['user_id']
