from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .services import get_all_chats

# @api_view(["POST"])
# def create_or_join_chat(request):
#     user = request.user
#     chat_to = request.data['chat_to']

class ChatListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = get_all_chats(request.user)
        return "hello"