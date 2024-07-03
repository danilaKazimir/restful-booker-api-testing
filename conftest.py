import pytest
from faker import Faker
import requests

fake = Faker()


@pytest.fixture
def booking_data():
    def generate_booking_data():
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

    return generate_booking_data()


@pytest.fixture
def new_booking_data(booking_data):
    def create_booking():
        # Используем данные из booking_data
        data = booking_data

        # Отправляем POST запрос для создания бронирования и возвращаем ответ
        response = requests.post("https://restful-booker.herokuapp.com/booking", json=data)
        return response

    return create_booking
