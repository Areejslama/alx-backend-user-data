#!/usr/bin/env python3
"""this script to define flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


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


@app.route("/sessions",  methods=['POST'])
def login() -> str:
    """define method"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    valid_log = AUTH.valid_login("email","password")
    if not valid_log:
        abort(401)
        response = make_response(jsonify({"email": email,
                                      "message": "logged in"}))
        response.set_cookie('session_id', AUTH.create_session(email))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
