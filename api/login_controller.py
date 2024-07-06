from app import jwt
from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from create_app import bcrypt

login_bp = Blueprint("login_bp", __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = jwt.create_access_token(identity=username, additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token), 200
    return jsonify('Wrong username or password'), 401

@login_bp.route('/login', methods=['GET'])
@jwt_required
def protected():
    curr_user = get_jwt_identity()
    return jsonify(logged_in_as=curr_user)
