from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant


class TestHealthCheck(BaseApi):
    def test_send_ping(self):
        response = self.get(Constant.PING_ROUTE)

        Assertions.assert_code_status(response, 201)
        Assertions.assert_content(response, "Created")
