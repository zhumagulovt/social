from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from ..models import Comment, Post

User = get_user_model()


class CommentCreateTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )
        user.is_active = True
        user.save()

        Post.objects.create(content='This is a test post', user=user)
    
    def test_create_comment(self):
        user = User.objects.get(pk=1)

        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/api/v1/posts/1/add_comment/", data={"content": "This is a test post"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        
        comment = Comment.objects.all().first()
        post = Post.objects.get(pk=1)
        self.assertEqual(post.comments.all().first(), comment)