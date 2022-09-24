from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_all_chats, get_last_message, get_other_user_in_chat
from .serializers import ChatSerializer

# @api_view(["POST"])
# def create_or_join_chat(request):
#     user = request.user
#     chat_to = request.data['chat_to']

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
