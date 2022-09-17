from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from django.contrib.auth import get_user_model

from .views import FollowingFeedView
from .models import Post

from accounts.models import UserFollowing

User = get_user_model()


class PostCreateTest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='test_user',
            email='test_user@test.com',
            password='Qwerty123'
        )
        user.is_active = True
        user.save()

    def test_create_post(self):
        user = User.objects.get(pk=1)
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/v1/posts/', data={
            'content': 'This is a test post'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
