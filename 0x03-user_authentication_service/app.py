#!/usr/bin/env python3
"""this script to define flask app"""
from flask import Flask, jsonify, request, abort, redirect
from flask.helpers import make_response
from auth import Auth
from user import User


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'])
def payload():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """define function"""
    if request.method == "POST":
        email = request.args.get("email")
        password = request.args.get("password")
    try:
        AUTH.register_user("email", "password")
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"})
    else:
        abort(400)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions, - email, - password
    Returns request with form data with email and password fields
    """
    user_request = request.form
    user_email = user_request.get('email', '')
    user_password = user_request.get('password', '')
    valid_log = AUTH.valid_login(user_email, user_password)
    if not valid_log:
        abort(401)
    response = make_response(jsonify({"email": user_email,
                                      "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """define method to logout"""
    new_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(new_cookie)
    if new_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """define method"""
    new_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(new_cookie)
    if new_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """define method"""
    email = request.form.get("email")
    is_registered = AUTH.create_session(email)
    if not is_registered:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """define method"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    except Exception:
        abort(500)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
