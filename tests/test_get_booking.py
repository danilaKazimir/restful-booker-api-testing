from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestGetBooking(BaseApi):
    ROUTE = "/booking/"

    def test_get_existing_booking(self, create_booking_data):
        booking_data = create_booking_data
        response1 = self.create_new_booking(self.ROUTE, booking_data)

        Assertions.assert_code_status(response1, 200)

        booking_id = self.get_booking_id(response1)

        response2 = self.get(f"{self.ROUTE}{booking_id}")

        Assertions.assert_code_status(response2, 200)
        assert response2.json() == booking_data

    def test_get_nonexistent_booking(self):
        response = self.get(f"{self.ROUTE}0")

        Assertions.assert_code_status(response, 404)
        Assertions.assert_content(response, "Not Found")
