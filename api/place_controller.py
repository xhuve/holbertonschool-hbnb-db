import sys
import os

from models.user import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity
from app import app


place_bp = Blueprint('place_bp', __name__)

@place_bp.route('/places', methods=['GET'])
def get_all_places():
    return DataManager.all(Place)

@place_bp.route('/places', methods=['POST'])
def create_place():
    jData = request.get_json()
    if not -90 < jData["latitude"] < 90 or not isinstance(jData["price_per_night"], float):
        print("latitude error")
        return jsonify("Bad Request"), 400
    for field in ['number_of_rooms', 'bathrooms', 'max_guests']:
        if jData[field] < 0:
            return jsonify("Bad Request"), 400

    amenity_ids = jData.get("amenity_ids", [])
    if not all(isinstance(amenity_id, int) for amenity_id in amenity_ids):
        return jsonify("Bad Request"), 400

    all_city_id = [value for value in DataManager.all(City) if value["id"] == jData["city_id"]]
    if not all_city_id:
        return jsonify("Bad Request"), 400

    all_amenity_id = [value for value in DataManager.all(Amenity) if value["id"] in jData["amenity_id"]]
    if not all_amenity_id:
        return jsonify("Bad Request"), 400

    place = Place(
        name = jData['name'],
        description = jData['description'],
        address = jData['address'],
        longitude = jData['longitude'],
        latitude = jData['latitude'],
        price_per_night = jData['price_per_night'],
        number_of_rooms = jData["number_of_rooms"],
        bathrooms = jData["bathrooms"],
        max_guests = jData["max_guests"],
        amenity_ids = amenity_ids,
        city_id = jData["city_id"],
        host_id = jData["host_id"]
    )

    return DataManager.save(place), 201

@place_bp.route('/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    return DataManager.get(place_id, Place)

@place_bp.route('/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    jData = request.get_json()
    if not -90 < jData["latitude"] < 90 or not isinstance(jData["price_per_night"], int):
        return jsonify("Bad Request"), 400
    for field in ['number_of_rooms', 'bathrooms', 'max_guests']:
        if jData[field] < 0:
            return jsonify("Bad Request"), 400

    req_place = DataManager.get(place_id, Place)
    if not req_place:
        return jsonify("Bad Request"), 400

    city = DataManager.get(jData["city_id"], City)
    if not city:
        return jsonify("Bad Request"), 400

    place = Place(
        name = jData['name'],
        description = jData['description'],
        address = jData['address'],
        longitude = jData['longitude'],
        latitude = jData['latitude'],
        price_per_night = jData['price_per_night'],
        number_of_rooms = jData["number_of_rooms"],
        bathrooms = jData["bathrooms"],
        max_guests = jData["max_guests"] ,
        amenity_id= jData.get("amenity_id", []),
        city_id= jData["city_id"],
        host_id= jData['host_id']
    )

    place.id = place_id
    place.created_at = req_place["created_at"]

    try:
        DataManager.update(place)
        return jsonify("Updated")
    except Exception:
        return jsonify("Bad Request"), 400

@place_bp.route('/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    DataManager.delete(place_id, Place)
    return jsonify("Deleted"), 204

@place_bp.route("/places/<int:place_id>/reviews", methods=['POST'])
def create_review(place_id):
    jData = request.get_json()

    review = Review(
        feedback = jData['feedback'],
        rating = jData['rating'],
        comment = jData['comment'],
        place_id = place_id,
        user_id = jData["user_id"]
    )

    return DataManager.save(review), 201

@place_bp.route("/places/<int:place_id>/reviews", methods=['GET'])
def get_place_reviews(place_id):
    all_reviews = DataManager.all(Review)

    if not place_id in [value["id"] for value in DataManager.all(User)]:
        return jsonify("User not found"), 404

    user_reviews = [review for review in all_reviews if review["place_id"] == place_id]

    return jsonify(user_reviews), 200
