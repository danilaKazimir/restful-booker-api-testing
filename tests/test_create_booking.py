from lib.base_api import BaseApi


class TestCreateBooking(BaseApi):
    BOOKING_ROUTE = "/booking"

    def test_create_new_booking(self, create_new_booking, create_booking_data):
        create_new_booking(create_booking_data)
