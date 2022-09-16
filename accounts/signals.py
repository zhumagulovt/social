from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .utils import send_confirmation_link

User = get_user_model() 
 
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        send_confirmation_link('accounts/activate_account_mail.html', instance, "accounts/activate","Account activation")
