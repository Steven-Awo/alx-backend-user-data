#!/usr/bin/env python3
""" Modules thats for Users views
"""
from api.v1.views import app_views

from flask import abort, jsonify, request

from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - the list for all the User objects thats in
      JSON represented
    """
    all_the_users = [userr.to_json() for userr in User.all()]
    return jsonify(all_the_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET thats in /api/v1/users/:id
    Path parameter:
      - the user's ID
    Return:
      - The user thats for the object in
      JSON represented
      - 404 thats if the User's ID doesn't actually exist
    """
    if user_id is None:
        abort(404)

    userr = User.get(user_id)

    if userr is None:
        abort(404)
    return jsonify(userr.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE for /api/v1/users/:id
    Path parameter:
      - User's ID
    Return:
      - the empty JSON is that the User has already
      been correctly removed or deleted
      - 404 thats if the User's ID doesn't exist
    """
    if user_id is None:
        abort(404)

    userr = User.get(user_id)

    if userr is None:
        abort(404)

    userr.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rmjsn = None
    the_error_mssg = None

    try:
        rmjsn = request.get_json()
    except Exception as e:
        rmjsn = None
    if rmjsn is None:
        the_error_mssg = "Wrong format"

    if the_error_mssg is None and rmjsn.get("email", "") == "":
        the_error_mssg = "email missing"

    if the_error_mssg is None and rmjsn.get("password", "") == "":
        the_error_mssg = "password missing"
    if the_error_mssg is None:
        try:
            userr = User()
            userr.email = rmjsn.get("email")
            userr.password = rmjsn.get("password")
            userr.first_name = rmjsn.get("first_name")
            userr.last_name = rmjsn.get("last_name")
            userr.save()
            return jsonify(userr.to_json()), 201
        except Exception as e:
            the_error_mssg = "Can't create User: {}".format(e)
    return jsonify({'error': the_error_mssg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT thats for /api/v1/users/:id
    Path parameter:
      - User's ID
    JSON body:
      - the user's last_name (optional)
      - the user's first_name (optional)
    Return:
      - the user's object thats JSON represented
      - 404 thats if the User's ID actually doesn't exist
      - 400 thats if can't actually be updated the User
    """
    if user_id is None:
        abort(404)

    userr = User.get(user_id)

    if userr is None:
        abort(404)
    rmjsn = None

    try:
        rmjsn = request.get_json()
    except Exception as e:
        rmjsn = None

    if rmjsn is None:
        return jsonify({'error': "Wrong format"}), 400

    if rmjsn.get('first_name') is not None:
        userr.first_name = rmjsn.get('first_name')

    if rmjsn.get('last_name') is not None:
        userr.last_name = rmjsn.get('last_name')
    userr.save()
    return jsonify(userr.to_json()), 200
