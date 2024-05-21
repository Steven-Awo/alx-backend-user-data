#!/usr/bin/env python3
"""manage the API authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Creating the BasicAuth's Class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """This returning the Base64 part thats of the actually
        Authorization header"""
        if authorization_header is None or\
           type(authorization_header) is not str:
            return None
        hdr = authorization_header.split(' ')

        return hdr[1] if hdr[0] == 'Basic' else None

