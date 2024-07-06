from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from sqlalchemy import text
from models import db

load_dotenv()

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    import os

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config["USE_DATABASE"] = os.getenv("USE_DATABASE", False)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_FLAVOUR", "sqlite:///in-memory")

    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)


    if app.config["USE_DATABASE"]:
        with app.app_context():
            db.drop_all()
            db.create_all()

            from api.amenity_controller import amenity_bp
            from api.country_controller import country_bp
            from api.city_controller import city_bp
            from api.place_controller import place_bp
            from api.user_controller import user_bp
            from api.review_controller import review_bp

            app.register_blueprint(amenity_bp)
            app.register_blueprint(country_bp)
            app.register_blueprint(city_bp)
            app.register_blueprint(place_bp)
            app.register_blueprint(user_bp)
            app.register_blueprint(review_bp)

    return app, db, jwt