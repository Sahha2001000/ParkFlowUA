from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.parking import City, Parking, Spot

class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = City
        load_instance = True

class ParkingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Parking
        load_instance = True
        include_fk = True

class SpotSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Spot
        load_instance = True
        include_fk = True