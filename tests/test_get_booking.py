from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestGetBooking(BaseApi):
    def test_get_existing_booking(self, create_booking_data, create_new_booking):
        booking_data = create_booking_data
        response = self.get(f"{Constant.BOOKING_ROUTE}{create_new_booking(booking_data)}")

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_obj_values(response, booking_data)

    def test_get_nonexistent_booking(self):
        response = self.get(f"{Constant.BOOKING_ROUTE}0")

        Assertions.assert_code_status(response, 404)
        Assertions.assert_content(response, "Not Found")
