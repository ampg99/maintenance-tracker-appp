from flask import abort, jsonify, request, json, Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
from ..model.models import User, UserSchema, Request
from ..model.user import UserStore
from ..model.initial import db, get_current_user
from mongoengine.errors import NotUniqueError, ValidationError
from passlib.handlers.bcrypt import bcrypt
from flask import Blueprint, make_response
import requests


USER = Blueprint("api.userAPI.user", __name__)


@USER.route("/create_account", methods=["POST"])
def create_user():
    """
    Create a new user and send an activation email
    """
    user, errors = db.users.is_valid(request.json)
    if errors:
        message = json.dumps({'errors': errors})
        return Response(message, status=422, mimetype='application/json')

    result = request.json
    user = User(result['username'], result['email'], result['password'])
    db.users.insert(user)
    headers = {"Content-type": "application/json"}
    return jsonify({"New_user": user.to_json_object()})

@USER.route("/login", methods=["POST"])
def post():
    """
    Login in the user and store the user id and token pair into redis
    """
    try:
        # Get user email and password. Was not checked cause none type has no attribute strip.
        email, password = request.json.get('username').strip(), request.json.get('password').strip()
    except Exception as e:
        return {"Status": "error", "Message": e}

    user = db.users.query_by_field("username", request.json.get("username"))

    if not user:
        response =  {"status": "error", "message": "Username does not exist"}
        return jsonify(response), 400
        
    elif not bcrypt.verify(request.json.get("password"), user.password):
        response =  {"status": "error", "message": "The password you provided is wrong"}
        return jsonify(response), 400

    login_token = create_access_token(identity=user.username)
    return jsonify({
        "status": "successfull login",
        "details": {
            "login_token": login_token,
            "user": user.to_json_object()
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
    return jsonify({"status": "request sent successfully","data": {"request": a_request.to_json_object()}}), 201

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
    maintenance_request = db.requests.query(_id)
    if maintenance_request is None:
        return jsonify({
            "status": "error",
            "message": "Maintenance request does not exist"
        }), 404
    elif maintenance_request.created_by.username != get_jwt_identity():
        return jsonify({
            "status": "error",
            "message": "You are not allowed to modify or view this maintenance request"
        }), 401
    else:
        if request.method == "PUT":
            if request.is_json:
                valid, errors = db.requests.is_valid(request.json)
                if not valid:
                    return jsonify({
                        "status": "error",
                        "data": errors
                    }), 400
                result = request.json

                maintenance_request.requestname = result['requestname']
                maintenance_request.description = result['description']
            else:
                return jsonify({
                    "message": "Request should be in JSON",
                    "status": "error"
                }), 400

        return jsonify({
            "status": "success",
            "data": {
                "request": maintenance_request.to_json_object()}
        }), 200