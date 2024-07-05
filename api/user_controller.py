import sys
import os

from flask_jwt_extended import get_jwt_identity, jwt_required

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

@user_bp.route('/users', methods=['GET'], endpoint='get_all_users')
def get_all_users():
    return DataManager.all(User)

@user_bp.route('/users', methods=['POST'], endpoint='create_user')
# @jwt_required
def create_user():
    # curr_user = get_jwt_identity()
    # if not curr_user.is_admin:
    #     return jsonify("User does not have admin privileges"), 403

    jData = request.get_json()
    for field in ["email", "first_name", "last_name"]:
        if not isinstance(jData[field], str):
            return jsonify("Bad Request"), 400
    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400
    if not os.getenv("USE_DATABASE") and jData["email"] in User.email_list:
        return jsonify("Conflict"), 409

    user = User(
        email=jData["email"],
        password=jData["password"],
        first_name=jData["first_name"],
        last_name=jData["last_name"],
        city_id=jData["city_id"]
    )
    return DataManager.save(user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'], endpoint='get_user')
def get_user(user_id):
    return DataManager.get(user_id, User)

@user_bp.route('/users/<int:user_id>', methods=['PUT'], endpoint='update_user')
@jwt_required
def update_user(user_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

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

@user_bp.route('/users/<int:user_id>', methods=['DELETE'], endpoint='delete_user')
@jwt_required
def delete_user(user_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    DataManager.delete(user_id, User)
    return jsonify("Deleted"), 204

@user_bp.route('/users/<int:user_id>/reviews', methods=['GET'], endpoint='get_user_reviews')
def get_user_reviews(user_id):
    all_reviews = DataManager.all(Review)

    if not user_id in [value["id"] for value in DataManager.all(User)]:
        return jsonify("User not found"), 404

    user_reviews = [review for review in all_reviews if review["user_id"] == user_id]

    return jsonify(user_reviews), 200
