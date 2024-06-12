import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.city import City
from country_controller import get_city_in_country


app = Flask(__name__)
dm = DataManager()

@app.route('/cities', methods=['GET'])
def get_all_cities():
    return DataManager.storage["City"]

@app.route('/cities', methods=['POST'])
def create_city():
    jData = request.get_json()
    if not isinstance(jData["name"], str) or not isinstance(jData["population"], int):
        return jsonify("Bad Request"), 400

    dictionary = get_city_in_country(jData["country_code"])
    for item in dictionary:
        if item["name"] == jData["name"]:
            return jsonify("Bad Request"), 400

    city = City(
        name=jData["name"],
        population=jData["population"],
        country_code=jData["country_code"]
    )
    return dm.save(city), 201

@app.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    curr_city = dm.get(city_id, "City")
    return { "name": curr_city["name"], "country_code": curr_city["country_code"]}

@app.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    jData = request.get_json()
    req_city = dm.get(city_id, "City")

    city = City(
        name=jData['name'],
        population=jData['population'],
        country_code=jData['country_code']
    )

    city.id = city_id
    city.created_at = req_city["created_at"]

    try:
        dm.update(city)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400


@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_cities(city_id):
    dm.delete(city_id, "City")
    return jsonify("Deleted"), 204

if __name__ == '__main__':
    app.run(debug=True)