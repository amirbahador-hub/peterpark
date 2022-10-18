from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plate(db.Model):
    __tablename__ = "plates"
    raw_plate = db.Column(db.String, primary_key=True, index=True)
    plate_without_hyphen = db.Column(db.String)
    timestamp = db.Column(db.TIMESTAMP)

    def __repr__(self) -> str:
        return "Plate>>> {self.raw_plate}"
