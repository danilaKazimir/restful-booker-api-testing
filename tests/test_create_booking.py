import requests
from lib.base_class import BaseClass
from lib.assertions import Assertions


class TestCreateBooking(BaseClass):
    def test_create_new_booking(self, new_booking_data):
        response = new_booking_data()
        print(response.text)
        assert response.status_code == 200

        main_keys = ["bookingid", "booking"]
        Assertions.assert_json_has_keys(response, main_keys)
