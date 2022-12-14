from flask.json import jsonify
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from flask import Flask
import os
from src.core import core
from src.database import db
from flasgger import Swagger
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI", "postgresql://peterpark:pass@localhost"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SWAGGER={"title": "Plate API", "uiversion": 3},
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    app.register_blueprint(core)

    Swagger(app, config=swagger_config, template=template)
    with app.app_context():
        db.create_all()

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify({"error": "Something went wrong, we are working on it"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app

