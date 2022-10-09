from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from ..serializers import UserDetailSerializer, UserEditSerializer

User = get_user_model()


class UserDetailView(generics.RetrieveAPIView):
    """Get detail info about user"""
    lookup_field = "username"
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserEditView(generics.UpdateAPIView):
    """Edit user"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer

    def get_object(self):
        return self.request.user


class UserDeleteAvatarView(APIView):
    """View for deleting profile picture"""
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=None,
        responses=None
    )
    def post(self, request):
        user = request.user
        user.avatar = "avatars/default.jpg"
        user.save()
        return Response(status=status.HTTP_200_OK)
