import pytest
from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestDeleteBooking(BaseApi):
    def test_delete_booking_using_cookie_value(self, create_booking_data, create_new_booking, get_auth_token):
        booking_id = create_new_booking(create_booking_data)

        response = self.delete(
            f"{Constant.BOOKING_ROUTE}{booking_id}",
            headers={"Cookie": f"token={get_auth_token()}"}
        )

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")

        # Checking that the booking is deleted
        get_response = self.get(f"{Constant.BOOKING_ROUTE}{booking_id}")

        Assertions.assert_code_status(get_response, 404)
        Assertions.assert_content(get_response, "Not Found")

    def test_delete_booking_using_authorization_header(self, create_booking_data, create_new_booking):
        booking_id = create_new_booking(create_booking_data)

        response = self.delete(
            f"{Constant.BOOKING_ROUTE}{booking_id}",
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")

        # Checking that the booking is deleted
        get_response = self.get(f"{Constant.BOOKING_ROUTE}{booking_id}")

        Assertions.assert_code_status(get_response, 404)
        Assertions.assert_content(get_response, "Not Found")

    @pytest.mark.delete_data_after_test
    def test_delete_booking_without_headers(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}"
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    @pytest.mark.delete_data_after_test
    def test_delete_booking_with_invalid_cookie(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Cookie": "invalid_cookie"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    @pytest.mark.delete_data_after_test
    def test_delete_booking_with_invalid_auth_header(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{Constant.BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Authorization": "invalid_auth_value"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_delete_nonexistent_booking(self):
        response = self.delete(
            f"{Constant.BOOKING_ROUTE}0",
            headers={"Authorization": Constant.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 405)
        Assertions.assert_content(response, "Method Not Allowed")
