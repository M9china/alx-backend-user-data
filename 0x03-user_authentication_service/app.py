#!/usr/bin/env python3
"""Flask application module"""

from flask import Flask, jsonify, request, session
import flask
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello() -> str:
    """GET /
    Return: welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """route to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password is required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """route to login a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password is required"}), 400

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            return jsonify({"email": email, "message": "logged in"}), 200
    return flask.abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """route to logout a user"""
    session_id = request.cookies.get('session_id')
    if session:
        AUTH.destroy_session(session_id)
        return flask.redirect('/')
    return flask.abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
