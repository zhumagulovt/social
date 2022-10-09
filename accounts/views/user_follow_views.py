from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import *

User = get_user_model()


class UserFollowView(APIView):
    """View for follow or unfollow from user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user = request.user
        to_follow = User.objects.get(username=username)

        if user == to_follow:
            return Response("User can't follow himself", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if to_follow in user.following.all():
            # unfollow
            user.following.remove(to_follow)
        else:
            # follow
            user.following.add(to_follow)

        return Response(status=status.HTTP_200_OK)


class UserFollowingListView(generics.ListAPIView):
    """View for getting list of followings"""

    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        queryset = User.objects.filter(followers__user=user)
        return queryset


class UserFollowerListView(generics.ListAPIView):
    """View for getting list of followers"""

    serializer_class = UserSerializer

    def get_queryset(self):
        
        user = User.objects.get(username=self.kwargs.get('username'))
        # in models user's related name is following
        queryset = User.objects.filter(following__following=user)
        return queryset
