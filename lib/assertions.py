import json
from requests import Response


class Assertions:
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
