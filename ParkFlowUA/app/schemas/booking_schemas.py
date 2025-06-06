from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.booking import Booking

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
