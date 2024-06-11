import sys
import os
from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.amenity import Amenity

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

app = Flask(__name__)
dm = DataManager()

@app.route('/amenities', methods=['GET'])
def get_all_amenities():
    return DataManager.storage["Amenity"]

@app.route('/amenities', methods=['POST'])
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
    return dm.save(amenity), 201

@app.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    return dm.get(int(amenity_id), "Amenity")

@app.route('/amenities/<string:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    jData = request.get_json()
    req_amenity = dm.get(amenity_id, "Amenity")

    amenity = Amenity(
        name=jData["name"],
        description=jData["description"],
        place_id=jData["place_id"],
    )

    amenity.id = amenity_id
    amenity.created_at = req_amenity["created_at"]

    try:
        dm.update(amenity)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@app.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    dm.delete(amenity_id, "Amenity")
    return jsonify("Deleted"), 204
