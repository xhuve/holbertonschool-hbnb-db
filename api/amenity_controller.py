import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.amenity import Amenity

amenity_bp = Blueprint("amenity", __name__)

@amenity_bp.route('/amenities', methods=['GET'])
def get_all_amenities():
    return DataManager.all(Amenity)

@amenity_bp.route('/amenities', methods=['POST'])
def create_amenity():
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

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    return DataManager.get(amenity_id, Amenity)

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['PUT'])
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

@amenity_bp.route('/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    DataManager.delete(amenity_id, Amenity)
    return jsonify("Deleted"), 204
