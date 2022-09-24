from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_all_chats, get_all_messages, \
    get_last_message, get_other_user_in_chat, create_chat_if_not_exists

from .serializers import ChatSerializer, ChatDetailSerializer

# @api_view(["POST"])
# def create_or_join_chat(request):
#     user = request.user
#     chat_to = request.data['chat_to']
User = get_user_model()


class ChatListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = []
        chats = get_all_chats(request.user)

        for chat in chats:
            user2 = get_other_user_in_chat(request.user, chat)
            last_message = get_last_message(request.user, user2)
            
            serializer = ChatSerializer({'user': user2, 'last_message': last_message})
            result.append(serializer.data)

        return Response({"chats": result})


class ChatDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        user2 = User.objects.filter(pk=pk).first()

        if user2 and user2 != request.user:

            create_chat_if_not_exists(request.user, user2)

            messages = get_all_messages(request.user, user2)

            serializer = ChatDetailSerializer({'user': user2, 'messages': messages})

            return Response(serializer.data)

        raise ValidationError()