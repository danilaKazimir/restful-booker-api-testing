import pytest
from lib.base_api import BaseApi
from lib.assertions import Assertions


class TestCreateToken(BaseApi):
    CREATE_TOKEN_ROUTE = "/auth"
    VALID_ADMIN_DATA = {
        "username": "admin",
        "password": "password123"
    }
    invalid_admin_data = [
        {
            "username": "invalid_email",
            "password": "password123"
        },
        {
            "username": "admin",
            "password": "invalid_password"
        },
        {
            "username": "invalid_username",
            "password": "invalid_password"
        },
        {
            "username": None,
            "password": "password123"
        },
        {
            "username": "admin",
            "password": None
        },
        {
            "username": None,
            "password": None
        }
    ]

    def test_get_auth_token(self):
        response = self.post(self.CREATE_TOKEN_ROUTE, self.VALID_ADMIN_DATA)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, ["token"])

    @pytest.mark.parametrize("data", invalid_admin_data)
    def test_get_auth_token_with_invalid_admin_data(self, data):
        response = self.post(self.CREATE_TOKEN_ROUTE, data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_value_by_name(
            response,
            "reason",
            "Bad credentials",
            "Invalid reason message!"
        )
