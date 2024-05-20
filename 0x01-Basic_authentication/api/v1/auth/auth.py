#!/usr/bin/env python3
""" Setting up the Api's authentication
"""
from flask import request

from typing import List, TypeVar


class Auth():
    """ Creating the API authentication classb that manages it"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ This help to require the authorithation checks"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        if path[-1] != '/':
            path += '/'

        for a in excluded_paths:
            if a.endswith('*'):
                if path.startswith(a[:1]):
                    return False

        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """This is the authorization for the header checks"""
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ It chexk for the current user's method"""
        return None
