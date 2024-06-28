import sys
import os

from models.review import Review

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.user import User
from email_validator import validate_email, EmailNotValidError # type: ignore

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
    return DataManager.all(User)

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
        last_name=jData["last_name"],
        review_id=jData["review_id"],
        place_id=jData["place_id"]
    )
    return DataManager.save(user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return DataManager.get(user_id, User)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    jData = request.get_json()
    req_user = DataManager.get(user_id, User)

    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400

    user = User(
        email=jData["email"],
        first_name=jData["first_name"],
        last_name=jData["last_name"],
        review_id=jData["review_id"],
        place_id=jData["place_id"]
    )

    user.id = user_id
    user.created_at = req_user["created_at"]

    try:
        DataManager.update(user)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    DataManager.delete(user_id, User)
    return jsonify("Deleted"), 204

@user_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    all_reviews = DataManager.all(Review)

    if not user_id in [value["id"] for value in DataManager.all(User)]:
        return jsonify("User not found"), 404

    user_reviews = [review for review in all_reviews if review["user_id"] == user_id]

    return jsonify(user_reviews), 200

