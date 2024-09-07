#!/usr/bin/env python3
"""this script to Create a new Flask view"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv



@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def get_user() -> str:
    """Handle user login."""
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        session_name = getenv('SESSION_NAME')

        response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def destroy() -> str:
    """define method"""
    from api.v1.app import auth
    destroyed_session = auth.destroy_session(request)
    if destroyed_session is None:
        abort(404)
        return False
    return jsonify({}), 200
