#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.basic_auth import BasicAuth


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    auth = BasicAuth()
    user = auth.current_user(request)
    if not user:
        abort(403)
    all_users = [user.to_json() for user in User.all()]
    if not all_users:
        return jsonify({"users": []})
    return jsonify(all_users)
