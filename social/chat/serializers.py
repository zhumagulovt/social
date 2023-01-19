from rest_framework import serializers

from social.accounts.serializers import UserSerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "created_at", "text", "sender", "is_read"]


class ChatSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)


class ChatDetailSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    messages = MessageSerializer(read_only=True, many=True)
