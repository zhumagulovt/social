from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(
        "email address", 
        unique=True,
        error_messages={
            "unique": "This email is already in use"
        }
        )
    avatar = models.ImageField(default="avatars/default.jpg", upload_to="avatars/")
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserFollowing(models.Model):
    user = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'following']

    def __str__(self):
        return f"{self.user} -> {self.following}"
