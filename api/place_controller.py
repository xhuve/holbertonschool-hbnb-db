import sys
import os
from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.place import Place

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

app = Flask(__name__)
dm = DataManager()

@app.route('/places', methods=['GET'])
def get_all_places():
    return DataManager.storage["Places"]

@app.route('/places', methods=['POST'])
def create_place():
    jData = request.get_json()
    if not -90 < jData["latitude"] < 90 or not isinstance(jData["price_per_night"], int):
        return jsonify("Bad Request"), 400
    for field in ['number_of_rooms', 'bathrooms', 'max_guests']:
        if jData[field] < 0:
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
        max_guests = jData["max_guests"]
    )
    return dm.save(place), 201

@app.route('/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    return dm.get(place_id, "Place")

@app.route('/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    jData = request.get_json()
    req_city = dm.get(place_id, "Place")

    place = Place(
        name = jData['name'],
        description = jData['description'],
        address = jData['address'],
        longitude = jData['longitude'],
        latitude = jData['latitude'],
        price_per_night = jData['price_per_night'],
        number_of_rooms = jData["number_of_rooms"],
        bathrooms = jData["bathrooms"],
        max_guests = jData["max_guests"] 
    )

    place.id = place_id
    place.created_at = req_city["created_at"]

    try:
        dm.update(place)
        return jsonify("Updated")
    except Exception:
        return jsonify("Bad Request"), 400

@app.route('/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    dm.delete(place_id, "Place")
    return jsonify("Deleted"), 204

if __name__ == "__main__":
    app.run(debug=True)