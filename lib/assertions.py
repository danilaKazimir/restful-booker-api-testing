import json
from requests import Response


class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}, Actual: {response.status_code}"

    @staticmethod
    def assert_content(response: Response, expected_response):
        assert response.content.decode("utf-8") == expected_response, \
            f"Unexpected response content - '{response.content}', instead of - '{expected_response}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list, path=None):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response format is {response.text}"

        if path:
            keys = path.split('.')
            nested_dict = response_as_dict
            for key in keys:
                if key in nested_dict:
                    nested_dict = nested_dict[key]
                else:
                    assert False, f"Key '{path}' not found in the response JSON."

            for name in names:
                assert name in nested_dict, f"Key '{name}' not found in the nested JSON: {response_as_dict}"
        else:
            for name in names:
                assert name in response_as_dict, f"Key '{name}' not found in the response JSON: {response_as_dict}"

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response format is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_obj_values(response: Response, expected_obj_values: list, json_obj_path=None):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response format is {response.text}"

        if json_obj_path:
            keys = json_obj_path.split('.')
            nested_dict = response_as_dict
            for key in keys:
                if key in nested_dict:
                    nested_dict = nested_dict[key]
                else:
                    assert False, f"Key '{json_obj_path}' not found in the response JSON."

            assert expected_obj_values == nested_dict, \
                f"Incorrect JSON object in response! Expected - {expected_obj_values}, but is {nested_dict}"
        else:
            assert expected_obj_values == response_as_dict, \
                f"Incorrect JSON object in response! Expected - {expected_obj_values}, but is {response_as_dict}"
