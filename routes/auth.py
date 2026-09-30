from flask import Blueprint, request, jsonify
from services.user import(get_user, create_user, verify_password)
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,create_refresh_token
from services.user import email_validation

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name= data.get("name")
    email= data.get("email")
    password=data.get("password")
    if not name or not email or not password:
        return jsonify({"message": "Name,email and password are required"}),400
    existing_user = get_user(email)
    if existing_user:
        return jsonify({"message": "email already registered"}),400
    user_id = create_user(name,email,password)
    return jsonify({"message":"user registered successfully","user_id": user_id}),200

@auth_bp.route("/login", methods =["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "email and password required"}),400
    user = get_user(email)
    if not user:
        return jsonify({"message":"User does not exist"}),401
    user_id,name,email,password_hash = user
    if not verify_password(password_hash, password):
        return jsonify({"message":"Invalid email or password"}),401
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    return jsonify({"message":"Login successful", "access_token": access_token, "refresh_token":refresh_token}),200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id})

@auth_bp.route("/email",methods=["GET"])
def email_valid():
    data = request.get_json()
    Email = data['email']
    valid_email = email_validation(Email)
    if valid_email:
        return jsonify(True)
    return jsonify(False)

   