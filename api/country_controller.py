import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.country import Country

dm = DataManager()
country_bp = Blueprint("country", __name__)

@country_bp.route('/countries', methods=['GET'])
def get_all_countries():
    return DataManager.storage["Country"]

@country_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    return dm.get(country_id, "Country")

@country_bp.route("/countries/<string:country_code>/cities", methods=['GET'])
def get_city_in_country(country_code):
    if not country_code in Country.all_country_codes:
        return jsonify("Bad Request"), 400
    
    all_cities = [value for value in DataManager.storage["City"] if value["country_code"] == country_code]
    return all_cities

