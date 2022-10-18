from src.constants.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_409_CONFLICT,
)
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.database import Plate, db
from src.schemas import Search, PlateInput
from sqlalchemy import func
from sqlalchemy.exc import DatabaseError
from datetime import datetime
from flask_pydantic import validate
import re

core = Blueprint("core", __name__, url_prefix="/api/v1")


@core.get("/plate")
@swag_from("./docs/plate/get_plate.yaml")
def plate():
    response = list()
    for plate in Plate.query.all():
        response.append({"plate": plate.raw_plate, "timestamp": plate.timestamp})
    return jsonify(response)


@core.get("/search-plate")
@validate()
@swag_from("./docs/plate/search.yaml")
def search(query: Search):

    key = query.key
    levenshtein = query.levenshtein
    key = key.replace("-", "").upper()
    response = list()
    for plate in Plate.query.filter(
        func.levenshtein(Plate.plate_without_hyphen, key) <= levenshtein
    ).all():
        response.append({"plate": plate.raw_plate, "timestamp": plate.timestamp})
    return jsonify(response)


@core.post("/plate")
@validate()
@swag_from("./docs/plate/plate.yaml")
def create_plate(body: PlateInput):
    plate = body.raw_plate.upper()
    pattern = re.compile("^([A-Z]){1,3}-([A-Z]){1,2}([1-9])([0-9]){0,3}$")
    if not pattern.match(plate):

        return (
            jsonify({"error": "The plate is not a valid German plate"}),
            HTTP_422_UNPROCESSABLE_ENTITY,
        )
    new_plate = Plate(
        raw_plate=plate,
        plate_without_hyphen=plate.replace("-", ""),
        timestamp=datetime.now(),
    )
    db.session.add(instance=new_plate)
    try:
        db.session.commit()
    except DatabaseError as err:
        return jsonify({"error": str(err)}), HTTP_409_CONFLICT

    db.session.refresh(instance=new_plate)  # refresh attributes on the given instance
    return jsonify({"plate": new_plate.raw_plate, "timestamp": new_plate.timestamp}), HTTP_201_CREATED
