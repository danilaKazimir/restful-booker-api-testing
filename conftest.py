import pytest
from faker import Faker
from lib.base_api import BaseApi
from lib.assertions import Assertions
from constant import Constant

fake = Faker()
base = BaseApi()


@pytest.fixture
def create_booking_data():
    checkin_date = fake.date_between(start_date='-30d', end_date='today')
    checkout_date = fake.date_between_dates(
        date_start=checkin_date,
        date_end=checkin_date.replace(month=checkin_date.month + 1)
    )

    data = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.pyint(500, 1000),
        "depositpaid": fake.pybool(),
        "bookingdates": {
            "checkin": checkin_date.strftime('%Y-%m-%d'),
            "checkout": checkout_date.strftime('%Y-%m-%d')
        },
        "additionalneeds": fake.sentence(nb_words=10)
    }

    return data


@pytest.fixture
def generate_field_value():
    def _generate_field_value(field):
        if field == "firstname":
            return fake.first_name()
        elif field == "lastname":
            return fake.last_name()
        elif field == "totalprice":
            return fake.pyint(500, 1000)
        elif field == "depositpaid":
            return fake.pybool()
        elif field == "checkin" or field == "checkout":
            return fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d')
        elif field == "additionalneeds":
            return fake.sentence(nb_words=10)
        else:
            raise Exception(f"Invalid field value for generate field value method - {field}!")

    return _generate_field_value


@pytest.fixture
def create_new_booking(request):
    def _create_new_booking(data):
        response = base.post(f"{Constant.BOOKING_ROUTE}", data=data)

        Assertions.assert_code_status(response, 200)

        main_obj_keys = ["bookingid", "booking"]
        Assertions.assert_json_has_keys(response, main_obj_keys)

        booking_obj_keys = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "additionalneeds"]
        Assertions.assert_json_has_keys(response, booking_obj_keys, "booking")

        bookingdates_obj_keys = ["checkin", "checkout"]
        Assertions.assert_json_has_keys(response, bookingdates_obj_keys, "booking.bookingdates")

        Assertions.assert_json_obj_values(response, data, "booking")

        booking_id = base.get_json_value(response, "bookingid")

        def finalize():
            if "delete_data_after_test" in request.node.keywords:
                delete_response = base.delete(
                    f"{Constant.BOOKING_ROUTE}{booking_id}",
                    headers={"Authorization": Constant.AUTHORIZATION_VALUE}
                )
                Assertions.assert_code_status(delete_response, 201)
                Assertions.assert_content(delete_response, "Created")

        request.addfinalizer(finalize)

        return booking_id

    return _create_new_booking


@pytest.fixture
def get_auth_token():
    def _get_auth_token(data=None):
        if data is None:
            data = Constant.VALID_ADMIN_DATA
            response = base.post(Constant.TOKEN_ROUTE, data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_keys(response, ["token"])

            return base.get_json_value(response, "token")
        else:
            response = base.post(Constant.TOKEN_ROUTE, data)
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_value_by_name(
                response,
                "reason",
                "Bad credentials",
                "Invalid reason message!"
            )

    return _get_auth_token
