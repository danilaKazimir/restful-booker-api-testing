from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestCreateBooking(BaseApi):
    def test_create_new_booking(self, create_booking_data, create_new_booking):
        data = create_booking_data
        response = create_new_booking(data)

        Assertions.assert_code_status(response, 200)

        main_obj_keys = ["bookingid", "booking"]
        Assertions.assert_json_has_keys(response, main_obj_keys)

        booking_obj_keys = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "additionalneeds"]
        Assertions.assert_json_has_keys(response, booking_obj_keys, "booking")

        bookingdates_obj_keys = ["checkin", "checkout"]
        Assertions.assert_json_has_keys(response, bookingdates_obj_keys, "booking.bookingdates")
