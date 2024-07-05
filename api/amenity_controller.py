import sys
import os

from flask_jwt_extended import get_jwt_identity, jwt_required

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.amenity import Amenity

amenity_bp = Blueprint("amenity", __name__)

@amenity_bp.route('/amenities', methods=['GET'], endpoint="func1")
def get_all_amenities():
    return DataManager.all(Amenity)

@amenity_bp.route('/amenities', methods=['POST'], endpoint="func2")
@jwt_required
def create_amenity():
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    jData = request.get_json()
    for field in ["name", "description"]:
        if not isinstance(jData[field], str):
            return jsonify("Bad Request"), 400
    if not isinstance(jData["place_id"], int):
        return jsonify("Bad Request"), 400
    if jData["name"] in Amenity.amenity_list:
        return jsonify("Conflict"), 409

    amenity = Amenity(
        name=jData["name"],
        description=jData["description"],
        place_id=jData["place_id"]
    )
    return DataManager.save(amenity), 201

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['GET'], endpoint="func3")
def get_amenity(amenity_id):
    amenity = DataManager.get(amenity_id, Amenity)
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404
    return jsonify(amenity), 200

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['PUT'], endpoint="func4")
def update_amenity(amenity_id):
    jData = request.get_json()
    req_amenity = DataManager.get(amenity_id, Amenity)

    amenity = Amenity(
        name=jData["name"],
        description=jData["description"],
        place_id=jData["place_id"],
    )

    amenity.id = amenity_id
    amenity.created_at = req_amenity["created_at"]

    try:
        DataManager.update(amenity)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['DELETE'], endpoint="func5")
@jwt_required
def delete_amenity(amenity_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    DataManager.delete(amenity_id, Amenity)
    return jsonify("Deleted"), 204
