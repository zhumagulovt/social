from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from ..models import Saved, Post

User = get_user_model()


class SavedTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )
        self.user.is_active = True
        self.user.save()

        self.post = Post.objects.create(content='This is a test post', user=self.user)

    def test_post_save(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/posts/1/save/"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Saved.objects.count(), 1)
        self.assertEqual(self.post.saved.count(), 1)
    
    def test_post_unsave(self):
        Saved.objects.create(post=self.post, user=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/posts/1/save/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Saved.objects.count(), 0)
        self.assertEqual(self.post.saved.count(), 0)