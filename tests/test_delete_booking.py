from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestDeleteBooking(BaseApi):
    DELETE_BOOKING_ROUTE = "/booking/"
    AUTHORIZATION_VALUE = "Basic YWRtaW46cGFzc3dvcmQxMjM="

    def test_delete_booking_using_cookie_value(self, create_booking_data, create_new_booking, get_auth_token):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Cookie": f"token={get_auth_token()}"}
        )

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")

    def test_delete_booking_using_authorization_header(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Authorization": self.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")

    def test_delete_booking_without_headers(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}{create_new_booking(create_booking_data)}"
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_delete_booking_with_invalid_cookie(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Cookie": "invalid_cookie"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_delete_booking_with_invalid_auth_header(self, create_booking_data, create_new_booking):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}{create_new_booking(create_booking_data)}",
            headers={"Authorization": "invalid_auth_value"}
        )

        Assertions.assert_code_status(response, 403)
        Assertions.assert_content(response, "Forbidden")

    def test_delete_nonexistent_booking(self):
        response = self.delete(
            f"{self.DELETE_BOOKING_ROUTE}0",
            headers={"Authorization": self.AUTHORIZATION_VALUE}
        )

        Assertions.assert_code_status(response, 405)
        Assertions.assert_content(response, "Method Not Allowed")
