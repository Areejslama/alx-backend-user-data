#!/usr/bin/env python3
"""this script to define flask app"""
from flask import Flask, jsonify, request, abort
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """define method"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if not email or not password:
        abort(400)

    try:
        if not AUTH.valid_login(email, password):
            abort(401)

        session_id = AUTH.create_session(email)
        message = ({"email": email, "message": "logged in"})

        response = make_response(jsonify(message))
        response.set_cookie("session_id", session_id)

        return response

    except ValueError:
        abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
