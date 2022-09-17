from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='test_user',
            email='test_user@gmail.com',
            password='Qwerty123'
        )
        user.is_active = True
        user.save()

    
    def test_login(self):

        url = "/api/v1/accounts/login/"
        data = {'username': 'test_user', 'password': 'Qwerty123'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)