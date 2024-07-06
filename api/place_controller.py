import sys
import os

from flask_jwt_extended import get_jwt_identity, jwt_required


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.user import User
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity

place_bp = Blueprint('place_bp', __name__)

@place_bp.route('/places', methods=['GET'])
def get_all_places():
    allPlaces = DataManager.all(Place)
    if allPlaces:
        return jsonify([value.to_dict() for value in allPlaces])
    return jsonify("No places")

@place_bp.route('/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    return jsonify(DataManager.get(place_id, Place).to_dict())

@place_bp.route('/places', methods=['POST'])
@jwt_required
def create_place():
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    jData = request.get_json()

    if jData["host_id"] != curr_user.id:
        return jsonify("Ownership error")

    if not (-90 < jData["latitude"] < 90) or not isinstance(jData["price_per_night"], float):
        return jsonify("Bad Request"), 400

    for field in ['number_of_rooms', 'bathrooms', 'max_guests']:
        if jData[field] < 0:
            return jsonify("Bad Request"), 400

    amenity_ids = jData.get("amenity_id", [])
    if not all(isinstance(amenity_id, int) for amenity_id in amenity_ids):
        return jsonify("Bad Request"), 400

    if not DataManager.get(jData["city_id"], City):
        return jsonify("City does not exist"), 400

    if any(not DataManager.all(Amenity) for _ in amenity_ids):
        return jsonify("One or more amenities do not exist"), 400

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

    DataManager.save(place)
    return jsonify(place.to_dict()), 201

@place_bp.route('/places/<int:place_id>', methods=['PUT'], endpoint='update_place')
@jwt_required
def update_place(place_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

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

@place_bp.route('/places/<int:place_id>', methods=['DELETE'], endpoint='delete_place')
@jwt_required
def delete_place(place_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    DataManager.delete(place_id, Place)
    return jsonify("Deleted"), 204

@place_bp.route("/places/<int:place_id>/reviews", methods=['POST'], endpoint='create_review')
@jwt_required
def create_review(place_id):
    jData = request.get_json()

    review = Review(
        feedback = jData['feedback'],
        rating = jData['rating'],
        comment = jData['comment'],
        place_id = place_id,
        user_id = jData["user_id"]
    )

    DataManager.save(review)
    return jsonify(review.to_dict()), 201

@place_bp.route("/places/<int:place_id>/reviews", methods=['GET'], endpoint='get_place_reviews')
def get_place_reviews(place_id):
    all_reviews = DataManager.all(Review)

    if not place_id in [value["id"] for value in DataManager.all(User)]:
        return jsonify("User not found"), 404

    user_reviews = [review for review in all_reviews if review["place_id"] == place_id]

    return jsonify(user_reviews), 200

@place_bp.put("/places/<place_id>/reviews", endpoint='put_place_review')
@jwt_required
def put_place_review(place_id):
    curr_user = get_jwt_identity()
    all_reviews = DataManager.all(Review)

    req_review = [review for review in all_reviews if review["place_id"] == place_id and review["user_id"] == curr_user.id]

    if not req_review:
        return jsonify({"error": "Review not found"}), 404

    return jsonify(req_review), 200
