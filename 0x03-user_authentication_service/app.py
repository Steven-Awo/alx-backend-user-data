#!/usr/bin/env python3
"""
The creation of the Flask app
"""
from auth import Auth

from flask import Flask, jsonify

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET for the route's index

    Returns:
        str: json {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200
