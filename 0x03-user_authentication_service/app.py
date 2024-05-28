#!/usr/bin/env python3
"""
Creating the flask's map
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET route index

    Returns:
        str: json {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
