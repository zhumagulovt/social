from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import *
from ..models import UserFollowing

User = get_user_model()


class UserFollowView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user = request.user
        to_follow = User.objects.get(username=username)

        if user == to_follow:
            return Response("User can't follow himself", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if UserFollowing.objects.filter(user=user, following=to_follow).exists():
            # unfollow
            UserFollowing.objects.filter(user=user, following=to_follow).delete()
        else:
            # follow
            UserFollowing.objects.create(user=user, following=to_follow)

        return Response(status=status.HTTP_200_OK)


class UserFollowingListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        queryset = User.objects.filter(followers__user=user)
        return queryset


class UserFollowerListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        
        user = User.objects.get(username=self.kwargs.get('username'))
        # in models user's related name is following
        queryset = User.objects.filter(following__following=user)
        return queryset
