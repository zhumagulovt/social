from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from .models import Comment, Like, Post

User = get_user_model()


class PostCreateTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )
        user.is_active = True
        user.save()

    def test_create_post(self):
        user = User.objects.get(pk=1)

        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/api/v1/posts/", data={"content": "This is a test post"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)


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


class LikeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="Qwerty123"
        )
        self.user.is_active = True
        self.user.save()

        self.post = Post.objects.create(content='This is a test post', user=self.user)

    def test_post_like(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/posts/1/like/"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.post.likes.count(), 1)
    
    def test_post_unlike(self):
        Like.objects.create(post=self.post, user=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/posts/1/like/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(self.post.likes.count(), 0)