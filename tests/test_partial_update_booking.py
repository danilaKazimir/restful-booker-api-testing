import pytest
from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestPartialUpdateBooking(BaseApi):
    FIELDS = [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "checkin",
        "checkout",
        "additionalneeds"
    ]
    invalid_headers_values = [
        None,
        {"Cookie": "Invalid cookie"},
        {"Authorization": "Invalid auth value"}
    ]

    @pytest.mark.delete_data_after_test
    @pytest.mark.parametrize("field_for_update", FIELDS)
    def test_partial_update_booking_using_cookie_value(self, create_booking_data, create_new_booking, get_auth_token,
                                                       generate_field_value, field_for_update):
        booking_data_before_update = create_booking_data
        booking_id = create_new_booking(booking_data_before_update)

        booking_data_after_update = booking_data_before_update
        updated_value = generate_field_value(field_for_update)
        if field_for_update not in ["checkin", "checkout"]:
            booking_data_after_update[field_for_update] = updated_value
        else:
            booking_data_after_update['bookingdates'][field_for_update] = updated_value

        response = self.patch(
            f"{Constant.BOOKING_ROUTE}{booking_id}",
            data=booking_data_after_update,
            headers={"Cookie": f"token={get_auth_token()}"}
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_obj_values(response, booking_data_after_update)

    @pytest.mark.delete_data_after_test
    @pytest.mark.parametrize("field_for_update", FIELDS)
    def test_partial_update_booking_using_auth_header(self, create_booking_data, create_new_booking,
                                                      generate_field_value, field_for_update):

        booking_data_before_update = create_booking_data
        booking_id = create_new_booking(booking_data_before_update)

        booking_data_after_update = booking_data_before_update
        updated_value = generate_field_value(field_for_update)
        if field_for_update not in ["checkin", "checkout"]:
            booking_data_after_update[field_for_update] = updated_value
        else:
            booking_data_after_update['bookingdates'][field_for_update] = updated_value

        response = self.patch(
            f"{Constant.BOOKING_ROUTE}{booking_id}",
            data=booking_data_after_update,
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_obj_values(response, booking_data_after_update)

    @pytest.mark.parametrize("field_for_update, invalid_value", list(zip(FIELDS, invalid_headers_values)))
    def test_partial_update_booking_with_invalid_headers(self, create_booking_data, create_new_booking,
                                                         generate_field_value, field_for_update, invalid_value):
        booking_data_before_update = create_booking_data
        booking_id = create_new_booking(booking_data_before_update)

        booking_data_after_update = booking_data_before_update
        updated_value = generate_field_value(field_for_update)
        if field_for_update not in ["checkin", "checkout"]:
            booking_data_after_update[field_for_update] = updated_value
        else:
            booking_data_after_update['bookingdates'][field_for_update] = updated_value

        response = self.patch(
            f"{Constant.BOOKING_ROUTE}{booking_id}",
            data=booking_data_after_update,
            headers=invalid_value
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    @pytest.mark.parametrize("field_for_update", FIELDS)
    def test_partial_update_nonexistent_booking(self, create_booking_data, create_new_booking,
                                                generate_field_value, field_for_update):
        booking_data_for_update = create_booking_data
        updated_value = generate_field_value(field_for_update)
        if field_for_update not in ["checkin", "checkout"]:
            booking_data_for_update[field_for_update] = updated_value
        else:
            booking_data_for_update['bookingdates'][field_for_update] = updated_value

        response = self.patch(
            f"{Constant.BOOKING_ROUTE}0",
            data=booking_data_for_update,
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 405)
        Assertions.assert_content(response, "Method Not Allowed")
