#!/usr/bin/env python3
"""Session Authentication View"""
import os
from flask import Blueprint, jsonify, make_response, request
from models.user import User
from api.v1.auth.auth import Auth

# Create a new blueprint for session authentication
session_auth = Blueprint('session_auth', __name__,
                         url_prefix='/api/v1/auth_session')


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Login route for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for missing email or password
    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)
    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    # Retrieve User instance by email
    user = User.search({'email': email})
    if not user:
        return make_response(jsonify(
            {"error": "no user found for this email"}), 404)

    # Verify password
    user = user[0]  # Assuming search returns a list
    if not user.is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"}), 401)

    # Create session ID and set it in the response cookie
    from api.v1.app import auth  # Import here to avoid circular import issues
    session_id = auth.create_session(user.id)
    if not session_id:
        return make_response(jsonify({"error": "error creating session"}), 500)

    # Return user data with session cookie
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
