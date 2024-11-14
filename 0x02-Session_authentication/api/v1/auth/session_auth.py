#!/usr/bin/env python3
"""Session Authentication Class"""
import os
from flask import Blueprint, jsonify, make_response, request
from api.v1.auth.auth import Auth


# Create a new blueprint for session authentication
session_auth = Blueprint('session_auth', __name__,
                         url_prefix='/api/v1/auth_session')


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return make_response(jsonify({"error": "email missing"}), 400)
    if password is None:
        return make_response(jsonify({"error": "password missing"}), 400)

    from models.user import User
    user = User.search({'email': email})
    if not user:
        return make_response(jsonify(
            {"error": "no user found for this email"}), 404)

    if user is None or not user.is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"}), 401)

    session_id = Auth().create_session(user.id)
    if session_id is None:
        return make_response(jsonify({"error": "error creating session"}), 500)
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


class SessionAuth(Auth):
    """Session Authentication Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        from models.user import User
        return User.get(user_id)
