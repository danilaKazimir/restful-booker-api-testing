from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestCreateBooking(BaseApi):
    BOOKING_ROUTE = "/booking"

    def test_create_new_booking(self, create_booking_data):
        data = create_booking_data
        response = self.create_new_booking(self.BOOKING_ROUTE, data)

        Assertions.assert_code_status(response, 200)

        main_obj_keys = ["bookingid", "booking"]
        Assertions.assert_json_has_keys(response, main_obj_keys)

        booking_obj_keys = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "additionalneeds"]
        Assertions.assert_json_has_keys(response, booking_obj_keys, "booking")

        bookingdates_obj_keys = ["checkin", "checkout"]
        Assertions.assert_json_has_keys(response, bookingdates_obj_keys, "booking.bookingdates")
