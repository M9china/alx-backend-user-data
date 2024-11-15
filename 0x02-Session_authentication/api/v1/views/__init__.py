#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from api.v1.auth.session_auth import SessionAuth

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
app_views.register_blueprint(SessionAuth().session_auth)

from api.v1.views.index import *
from api.v1.views.users import *

User.load_from_file()
