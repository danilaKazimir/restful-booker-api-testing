import pytest
from faker import Faker
from lib.base_api import BaseApi

BOOKING_ROUTE = "/booking"
fake = Faker()


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
def create_new_booking():
    def _create_booking(data):
        response = BaseApi.post(BOOKING_ROUTE, data=data)
        return response

    return _create_booking
