import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask, request, jsonify
from persistence.data_manager import DataManager
from models.country import Country

app = Flask(__name__)
dm = DataManager()

@app.route('/countries', methods=['GET'])
def get_all_countries():
    return DataManager.storage["Country"]

@app.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    return dm.get(country_id, "Country")

@app.route("/countries/<string:country_code>/cities", methods=['GET'])
def get_city_in_country(country_code):
    if not country_code in Country.all_country_codes:
        return jsonify("Bad Request"), 400
    
    all_cities = [value for value in DataManager.storage["City"] if value["country_code"] == country_code]
    return all_cities

if __name__ == '__main__':
    app.run(debug=True)