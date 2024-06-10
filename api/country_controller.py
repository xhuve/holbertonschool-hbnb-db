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

@app.route('/countries/<string:country_id>', methods=['GET'])
def get_city(country_id):
    return dm.get(int(country_id), "Country")

if __name__ == '__main__':
    app.run(debug=True)