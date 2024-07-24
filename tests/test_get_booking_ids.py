import pytest
from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestGetBookingIds(BaseApi):
    @pytest.mark.delete_data_after_test
    def test_get_all_ids(self, create_booking_data, create_new_booking):
        booking_id = create_new_booking(create_booking_data)

        response = self.get(f"{Constant.BOOKING_ROUTE}")

        Assertions.assert_code_status(response, 200)
        Assertions.assert_expected_object_exist_in_json(response, {"bookingid": booking_id})

    @pytest.mark.delete_data_after_test
    def test_get_all_ids_filtered_by_name(self, create_booking_data, create_new_booking):
        booking_data = create_booking_data
        firstname = booking_data["firstname"]
        lastname = booking_data["lastname"]
        booking_id = create_new_booking(booking_data)

        response = self.get(
            f"{Constant.BOOKING_ROUTE}",
            data={
                "firstname": firstname,
                "lastname": lastname
            })

        Assertions.assert_code_status(response, 200)
        Assertions.assert_expected_object_exist_in_json(response, {"bookingid": booking_id})

    @pytest.mark.xfail
    # This test doesn't work properly, it's a bug
    def test_get_all_ids_filtered_by_checkin_checkout_date(self, create_booking_data, create_new_booking):
        booking_data = create_booking_data
        checkin = booking_data["bookingdates"]["checkin"]
        checkout = booking_data["bookingdates"]["checkout"]
        booking_id = create_new_booking(booking_data)

        response = self.get(
            f"{Constant.BOOKING_ROUTE}",
            data={
                "checkin": checkin,
                "checkout": checkout
            })

        Assertions.assert_code_status(response, 200)
        Assertions.assert_expected_object_exist_in_json(response, {"bookingid": booking_id})
