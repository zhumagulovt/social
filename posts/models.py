from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images/%Y/%m/%d/")


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["post", "user"]


class Saved(models.Model):
    post = models.ForeignKey(Post, related_name="saved", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="saved", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["post", "user"]
