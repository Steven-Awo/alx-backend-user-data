#!/usr/bin/env python3
"""
The creation of the Flask app
"""
from auth import Auth

from flask import Flask, jsonify, request

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET for the route's index

    Returns:
        str: json {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200

@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """POST thats the route for the user register

    Returns:
        str: the messege
    """
    email = request.form.get('email')

    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)

        return jsonify({"email": f"{email}", "message": "user created"}), 200

    except Exception:
        return jsonify({"messege": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
