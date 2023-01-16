from django.core import mail
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )

        user.is_active = True
        user.save()

    def test_login(self):

        url = "/api/v1/accounts/login/"
        data = {"username": "test_user", "password": "Qwerty123"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class UserRegistrationTestCase(APITestCase):
    def test_registration(self):
        url = "/api/v1/accounts/registration/"
        data = {
            "username": "test_user",
            "email": "test_user@test.com",
            "password": "Qwerty_123456",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class UserActivateTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )

    def parse_message(self, message):

        for i in range(len(message)):
            # Finding from where starts query args
            if message[i] == "?":
                message = message[i:]
                break

        for i in range(len(message)):
            # Finding where <a> tags hyperlink ends
            if message[i] == '"':
                message = message[:i]
                break

        # Split queries
        queries = message.split("&")

        # We got something like ['uid=MQ', 'token=Q4Fcs']
        # Split each of them
        uid = queries[0].split("=")[1]
        token = queries[1].split("=")[1]

        return uid, token

    def test_activate(self):
        # Before activating
        user = User.objects.get(pk=1)
        self.assertFalse(user.is_active)

        message = mail.outbox[0].body
        url = "/api/v1/accounts/activate/"

        uid, token = self.parse_message(message)
        data = {"uid": uid, "token": token}

        # send response to activate user
        self.client.post(url, data=data, format="json")

        # After activating
        user = User.objects.get(pk=1)
        self.assertTrue(user.is_active)
