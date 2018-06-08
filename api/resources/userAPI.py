from flask import abort, jsonify, request, json, Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
from ..model.models import User, Request
from ..model.user import UserStore
from ..model.initial import db, get_current_user
from mongoengine.errors import NotUniqueError, ValidationError
from passlib.handlers.bcrypt import bcrypt
from flask import Blueprint, make_response
import requests
import psycopg2
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse



USER = Blueprint("api.userAPI.user", __name__)


@USER.route("/auth/create_account", methods=["POST"])
def create_user():
    """
    Create a new user and send an activation email
    """ 
    user, errors = db.users.is_valid(request.json)
    if errors:
        message = json.dumps({'errors': errors})
        return Response(message, status=422, mimetype='application/json')

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    user = User(username, email, password)
    db.users.insert(user)
    headers = {"Content-type": "application/json"}
    return jsonify({"New_user": user.json_obj()})

@USER.route("/auth/login", methods=["POST"])
def post():
    """
    Login in the user and store the user id and token pair into redis
    """
    try:
        # Get user email and password. Was not checked cause none type has no attribute strip.
        email, password = request.json.get('username').strip(), request.json.get('password').strip()
    except Exception as e:
        return {"Status": "error", "Message": e}

    user = db.users.gey_by_field("username", request.json.get("username"))

    print('before if statement',type(request.json.get("password")))

    if not user:
        response =  {"status": "error", "message": "Username does not exist"}
        return jsonify(response), 400
    elif not bcrypt.verify( request.json.get("password"), user['password']):
        response =  {"status": "error", "message": "The password you provided is wrong"}
        return jsonify(response), 400

    login_token = create_access_token(identity=user['username'])
    return jsonify({
        "status": "successfull login",
        "details": {
            "login_token": login_token,
            "user": user
        }
    }), 200


@USER.route("/logout", methods=["DELETE"])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    db.blacklist.add(jti)
    return jsonify({
        "status": "success",
        "message": "Successfully logged out"
    }), 200


@USER.route("/requests", methods=["POST"])
@jwt_required
def create_a_new_request():
    result = request.json
    a_request = Request(title=result['title'],
                        description=result['description'],
                        created_by=get_current_user())
    db.requests.insert(a_request)
    return jsonify({"status": "request sent successfully","data": {"request": a_request.json_obj()}}), 201

@USER.route("/requests", methods=["GET"])
@jwt_required
def get_requests():
    requests = [x.to_json_object() for x in db.requests.query_all().values() if
                x.created_by.username == get_jwt_identity()]  # get requests for this user
    return jsonify({
        "status": "success",
        "data": {
            "total_requests": len(requests),
            "requests": requests
        }
    }), 200


@USER.route("/requests/<int:_id>", methods=["PUT", "GET"])
@jwt_required
def update_request(_id):
    request = db.requests.query(_id)
    if request is None:
        return jsonify({
            "status": "error",
            "message": "There is no request with such id."
        }), 404
    elif request.created_by.username != get_jwt_identity():
        return jsonify({
            "status": "error",
            "message": "Sorry, you are not the owner of this request"
        }), 401
    else:
        if request.method == "PUT":
            if request.is_json:
                ok, errors = db.requests.is_valid(request.json)
                if not ok:
                    return jsonify({
                        "status": "error",
                        "data": errors
                    }), 400
                result = request.json

                request.requestname = result['requestname']
                request.description = result['description']

        return jsonify({
            "status": "successfully updated request for{}".created_by.username,
            "data": {
                "request": request.json_obj()}
        }), 200
