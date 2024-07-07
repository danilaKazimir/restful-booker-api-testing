import pytest
from lib.base_api import BaseApi
from constant import Constant
from lib.assertions import Assertions


class TestCreateBooking(BaseApi):
    FIELDS = [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "checkin",
        "checkout"
    ]

    def test_create_new_booking(self, create_new_booking, create_booking_data):
        create_new_booking(create_booking_data)

    def test_create_new_booking_without_additional_needs_info(self, create_new_booking, create_booking_data):
        booking_data = create_booking_data
        booking_data['additionalneeds'] = ""
        create_new_booking(booking_data)

    def test_create_new_booking_without_additional_needs_field(self, create_new_booking, create_booking_data):
        booking_data = create_booking_data
        booking_data['additionalneeds'] = None
        create_new_booking(booking_data)

    @pytest.mark.parametrize("missing_fields", FIELDS)
    def test_create_new_booking_without_required_fields(self, create_booking_data, missing_fields):
        booking_data = create_booking_data
        if missing_fields not in ["checkin", "checkout"]:
            booking_data[missing_fields] = None
        else:
            booking_data['bookingdates'][missing_fields] = None

        response = self.post(f"{Constant.BOOKING_ROUTE}", booking_data)

        Assertions.assert_code_status(response, 500)
        Assertions.assert_content(response, "Internal Server Error")
