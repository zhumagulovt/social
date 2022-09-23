from django.db.models import Q

from .models import Chat, Message

def create_chat_if_not_exists(user1, user2):
    """Create new chat for two users if doesn't exist"""
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
    ).select_related('user1', 'user2')

    return chats

def create_new_message(sender, recipient, text):
    """Create new message"""
    create_chat_if_not_exists(sender, recipient)
    message = Message.objects.create(
        sender=sender,
        recipient=recipient,
        text=text
    )
    return message

def get_all_messages(user1, user2):
    messages = Message.objects.filter(
        Q(sender=user1, recipient=user2) | Q(sender=user2, recipient=user1)
    ).select_related('sender', 'recipient')
    
    return messages