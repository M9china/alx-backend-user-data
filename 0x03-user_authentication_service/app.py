#!/usr/bin/env python3
"""Flask application module"""

from flask import Flask, abort, jsonify, request, session
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
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie(key='session_id', value=session_id,
                                httponly=True, path='/')
            return response, 200

    flask.abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """route to logout a user"""
    session_id = request.cookies.get('session_id')
    if session:
        AUTH.destroy_session(session_id)
        return flask.redirect('/')
    return flask.abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """route to get the profile of a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return flask.abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """route to get reset password token"""
    email = request.form.get('email')
    if not email:
        return flask.abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        return jsonify({"message": "email not registered"}), 400


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """route to update password"""
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        if not email or not reset_token or not new_password:
            return jsonify({"error": "Missing"}), 400

        AUTH.update_password(email, reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
