#!/usr/bin/env python3
"""
The sessionDBAuth's class thats to manage the API's authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth

from models.user_session import UserSession

from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Creating the sessionExpAuth's class thas to manage
    the API's authentication
    """

    def create_session(self, user_id=None):
        """Creating the session to be used
        """
        if user_id:
            sessioning_id = super().create_session(user_id)
            us = UserSession(user_id=user_id, sessioning_id=sessioning_id)
            us.save()
            UserSession.save_to_file()
            return sessioning_id

    def user_id_for_session_id(self, session_id=None):
        """Getting the user's ID just from  the session
        """
        if not session_id:
            return None

        UserSession.load_from_file()

        userrss = UserSession.search({'session_id': session_id})

        for U in userrss:
            deltta = timedelta(seconds=self.session_duration)

            if U.created_at + deltta < datetime.now():
                return None

            return U.user_id

    def destroy_session(self, request=None):
        """Deleting the user's session / log out
        """
        if request:
            sessioning_id = self.session_cookie(request)

            if not sessioning_id:
                return False

            if not self.user_id_for_session_id(sessioning_id):
                return False

            userrss = UserSession.search({'sessioning_id': sessioning_id})

            for U in userrss:
                U.remove()

                UserSession.save_to_file()

                return True
        return False
