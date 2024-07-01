from app import jwt
from flask import request, Blueprint, jsonify
from models.user import User
from persistence.data_manager import DataManager
from flask_bcrypt import Bcrypt
from app import app

login_bp = Blueprint("login_bp", __name__)
bcrypt = Bcrypt(app)

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = jwt.create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401
