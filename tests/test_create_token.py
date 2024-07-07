import pytest
from lib.base_api import BaseApi


class TestCreateToken(BaseApi):
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

    def test_get_auth_token(self, get_auth_token):
        get_auth_token()

    @pytest.mark.parametrize("data", invalid_admin_data)
    def test_get_auth_token_with_invalid_admin_data(self, data, get_auth_token):
        get_auth_token(data)
