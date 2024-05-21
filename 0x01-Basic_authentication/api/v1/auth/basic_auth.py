#!/usr/bin/env python3
"""manage the API authentication"""
from api.v1.auth.auth import Auth

import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """The returning of the decoded value thats of a Base64's
        string"""
        if base64_authorization_header is None or\
           type(base64_authorization_header) is not str:
            return None
        try:
            the_base64s_bytes = base64_authorization_header.encode('utf-8')

            msge_bytes = base64.b64decode(the_base64s_bytes)

            msge = msge_bytes.decode('utf-8')

            return msge
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """The returning of the user's email and their password
        from the Base64's decoded valuees"""
        if not decoded_base64_authorization_header or\
           not isinstance(decoded_base64_authorization_header, str)\
           or ":" not in decoded_base64_authorization_header:
            return (None, None)

        extracting = decoded_base64_authorization_header.split(':', 1)

        return (extracting[0], extracting[1]) if extracting else (None, None)
