import json
import requests
from requests import Response
from lib.logger import Logger


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

    def patch(self, url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return BaseApi._send(url, data, headers, cookies, 'PATCH')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{BaseApi.BASE_URL}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=headers, cookies=cookies)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method} was received")

        Logger.add_response(response)

        return response

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]
