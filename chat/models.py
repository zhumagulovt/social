from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User1",
                              related_name="+")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User2",
                              related_name="+")

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', db_index=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
