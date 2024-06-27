import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.user import User
from email_validator import validate_email, EmailNotValidError # type: ignore

dm = DataManager()
user_bp = Blueprint('user', __name__)

def checkEmail(email):
    try:
        v = validate_email(email)
        return v["email"]
    except EmailNotValidError as e:
        print(str(e))
        return False

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    return DataManager.storage["Users"]

@user_bp.route('/users', methods=['POST'])
def create_user():
    jData = request.get_json()
    for field in ["email", "first_name", "last_name"]:
        if not isinstance(jData[field], str):
            return jsonify("Bad Request"), 400
    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400
    if jData["email"] in User.email_list:
        return jsonify("Conflict"), 409

    user = User(
        email=jData["email"],
        password="",
        first_name=jData["first_name"],
        last_name=jData["last_name"]
    )
    return dm.save(user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return dm.get(user_id, "Users")

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    jData = request.get_json()
    req_user = dm.get(user_id, "User")

    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400

    user = User(
        email=jData["email"],
        first_name=jData["first_name"],
        last_name=jData["last_name"],
    )

    user.id = user_id
    user.created_at = req_user["created_at"]

    try:
        dm.update(user)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    dm.delete(user_id, "Users")
    return jsonify("Deleted"), 204

@user_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    all_reviews = DataManager.storage["Review"]

    if not user_id in [value["id"] for value in DataManager.storage["Users"]]:
        return jsonify("User not found"), 404

    user_reviews = [review for review in all_reviews if review["user_id"] == user_id]

    return jsonify(user_reviews), 200

