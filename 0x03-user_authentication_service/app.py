#!/usr/bin/env python3
"""
The creation of the Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

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
    """POST that's the route for user registration

    Returns:
        str: the message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Setting up the login asspect

    Returns:
        str: the messege about the login status
    """
    email = request.form.get('email')

    password = request.form.get('password')

    validating_the_login = AUTH.valid_login(email, password)

    if not validating_the_login:
        abort(401)

    session_id = AUTH.create_session(email)

    respondings = jsonify({"email": f"{email}", "message": "logged in"})

    respondings.set_cookie('session_id', session_id)

    return respondings


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Creating the logout setup

    Return:
       str: the logout message
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)

        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Return the user's profile if the session_id is valid

    Returns:
        str: JSON payload with user email or error message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """the function for the get_reset_password token

    Return:
       str: message
    """
    email = request.form.get('email')

    user = AUTH.create_session(email)

    if not user:
        abort(403)

    else:
        token = AUTH.get_reset_password_token(email)

        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """the route to the update_password's function

    Return:
       str: the message
    """
    email = request.form.get('email')

    reset_token = request.form.get('reset_token')

    new_password = request.form.get('new_password')
    
    try:
        AUTH.update_password(reset_token, new_psw)

        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
