import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.users import Users
from email_validator import validate_email, EmailNotValidError # type: ignore

app = Flask(__name__)
dm = DataManager()

def checkEmail(email):
    try:
        v = validate_email(email)
        return v["email"]
    except EmailNotValidError as e:
        print(str(e))
        return False

@app.route('/users', methods=['GET'])
def get_all_users():
    return DataManager.storage["Users"]

@app.route('/users', methods=['POST'])
def create_user():
    jData = request.get_json()
    for field in ["email", "first_name", "last_name"]:
        if not isinstance(jData[field], str):
            return jsonify("Bad Request"), 400
    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400
    if jData["email"] in Users.email_list:
        return jsonify("Conflict"), 409

    user = Users(
        email=jData["email"],
        password="",
        first_name=jData["first_name"],
        last_name=jData["last_name"]
    )
    return dm.save(user), 201

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    return dm.get(int(user_id), "Users")

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    jData = request.get_json()
    req_city = dm.get(user_id, "City")

    if not checkEmail(jData["email"]):
        return jsonify("Bad Request"), 400

    user = Users(
        email=jData["email"],
        first_name=jData["first_name"],
        last_name=jData["last_name"],
    )

    user.id = user_id
    user.created_at = req_city["created_at"]

    try:
        dm.update(user)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    dm.delete(user_id, "Users")
    return jsonify("Deleted"), 204

if __name__ == "__main__":
    app.run(debug=True)
