from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestHealthCheck(BaseApi):
    ROUTE = "/ping"

    def test_send_ping(self):
        response = self.get(TestHealthCheck.ROUTE)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")
