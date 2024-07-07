from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestDeleteBooking(BaseApi):
    def test_update_booking_using_cookie_value(self, create_booking_data, create_new_booking, get_auth_token):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            data=booking_data_for_update,
            headers={"Cookie": f"token={get_auth_token()}"}
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_obj_values(response, booking_data_for_update)

    def test_update_booking_using_authorization_header(self, create_booking_data, create_new_booking):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            data=booking_data_for_update,
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_obj_values(response, booking_data_for_update)

    def test_update_booking_without_headers(self, create_booking_data, create_new_booking):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            data=booking_data_for_update
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_update_booking_with_invalid_cookie(self, create_booking_data, create_new_booking):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            data=booking_data_for_update,
            headers={"Cookie": "invalid_cookie"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_update_booking_with_invalid_auth_header(self, create_booking_data, create_new_booking):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            data=booking_data_for_update,
            headers={"Authorization": "invalid_auth_value"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_update_nonexistent_booking(self, create_booking_data):
        booking_data_for_update = create_booking_data

        response = self.put(
            f"{Constant.BOOKING_ROUTE}0",
            data=booking_data_for_update,
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 405)
        Assertions.assert_content(response, "Method Not Allowed")
