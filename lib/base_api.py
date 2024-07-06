import json

import requests
from requests import Response


class BaseApi:
    BASE_URL = "https://restful-booker.herokuapp.com"

    def post(self, url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return BaseApi._send(url, data, headers, cookies, 'POST')

    def get(self, url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return BaseApi._send(url, data, headers, cookies, 'GET')

    def put(self, url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return BaseApi._send(url, data, headers, cookies, 'PUT')

    def delete(self, url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return BaseApi._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{BaseApi.BASE_URL}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method} was received")

        return response

    def create_new_booking(self, url, data):
        response = self.post(url, data=data)
        return response

    def get_booking_id(self, response: Response):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response format is {response.text}"

        return response_as_dict['bookingid']

    def get_auth_token(self, response: Response):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response format is {response.text}"

        return response_as_dict['token']

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]
