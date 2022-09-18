from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import UserDetailSerializer, UserEditSerializer
from ..models import UserFollowing

User = get_user_model()


class UserDetailView(generics.RetrieveAPIView):
    lookup_field = "username"
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserEditView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer

    def get_object(self):
        return self.request.user


class UserDeleteAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.avatar = "avatars/default.jpg"
        user.save()
        return Response(status=status.HTTP_200_OK)
