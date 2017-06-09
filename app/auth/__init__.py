# app/auth/__init__.py

from flask import Blueprint

# Instantiate a Blueprint Object that represents the authentication Blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views
