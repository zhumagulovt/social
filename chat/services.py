from django.db.models import Q

from .models import Chat, Message

def create_chat_if_not_exists(user1, user2):
    if not Chat.objects.filter(
        Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).exists():
            Chat.objects.create(
                user1=user1,
                user2=user2
            )

def get_all_chats(user):
    """Get all chats of user"""
    chats = Chat.objects.filter(
        Q(user1=user) | Q(user2=user)
    )
    return chats