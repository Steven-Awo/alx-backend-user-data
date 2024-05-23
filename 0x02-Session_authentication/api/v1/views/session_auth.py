#!/usr/bin/env python3
""" Creating the module  thats of the session auth's views
"""
from api.v1.views import app_views

from models.user import User

from flask import  request, jsonify

from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST that for /auth_session/login
    Return:
     - The user's instance thats based on the email
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        userrs = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not userrs:
        return jsonify({"error": "no user found for this email"}), 404
    
    for U in userrs:
        if not U.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    
        from api.v1.app import auth
    
        sessioning_id = auth.create_session(U.id)
    
        outt = jsonify(U.to_json())
    
        outt.set_cookie(getenv('SESSION_NAME'), sessioning_id)
    
        return outt
    return jsonify({"error": "no user found for this email"}), 404
