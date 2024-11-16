#!/usr/bin/env python3
"""Session Authentication View"""
import os
from flask import Blueprint, jsonify, make_response, request
from models.user import User

# Create a new blueprint for session authentication
session_auth = Blueprint('session_auth', __name__,
                         url_prefix='/api/v1/auth_session')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles user login with session authentication."""
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    # If no user is found
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth to avoid circular import issues
    from api.v1.app import auth

    # Create a session for the user
    session_id = auth.create_session(user.id)

    # Return the user representation and set the session cookie
    response = jsonify(user.to_json())
    cookie_name = os.getenv("SESSION_NAME")
    response.set_cookie(cookie_name, session_id)
    return response


@session_auth.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout route for session authentication"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        return False, 404
    return make_response(jsonify({}), 200)
