import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy # type: ignore

from api.amenity_controller import amenity_bp
from api.country_controller import country_bp
from api.city_controller import city_bp
from api.place_controller import place_bp
from api.user_controller import user_bp
from api.review_controller import review_bp
 

app = Flask(__name__)
app.config["USE_DATABASE"] = os.getenv("USE_DATABASE", False)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb:///--"
db = SQLAlchemy(app)

if app.config["USE_DATABASE"]:
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()

app.register_blueprint(amenity_bp)
app.register_blueprint(country_bp)
app.register_blueprint(city_bp)
app.register_blueprint(place_bp)
app.register_blueprint(user_bp)
app.register_blueprint(review_bp)

