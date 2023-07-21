from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        result = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine"
        )
        result = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(result.status_code, 200)
        self.assertEquals(
            list(result.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(result, "taxi/manufacturer_list.html")


class PrivetDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "testuser",
            "license_number": "ABC12345",
            "first_name": "fime",
            "last_name": "lame",
            "password1": "test12345",
            "password2": "test12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEquals(new_user.first_name, form_data["first_name"])
        self.assertEquals(new_user.last_name, form_data["last_name"])
        self.assertEquals(new_user.license_number, form_data["license_number"])