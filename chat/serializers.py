from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Chat, Message


# class ChatSerializer(serializers.ModelSerializer):

#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Chat
#         fields = ['chat']


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['created_at', 'text', 'sender']


class ChatSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)


class ChatDetailSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    messages = MessageSerializer(read_only=True, many=True)
