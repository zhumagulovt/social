from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import *
from ..serializers import *
from ..permissions import IsOwnerOrReadOnly
from ..usecases import delete_or_create_user_m2m_post_model


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        post = Post.objects.get(pk=pk)
        user = request.user

        delete_or_create_user_m2m_post_model(Like, user, post)

        return Response(status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data
        data["post"] = pk
        data["user"] = request.user.pk
        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            Comment.objects.create(**serializer.validated_data)


class CommentDeleteView(DestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SavedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        delete_or_create_user_m2m_post_model(Saved, user, post)

        return Response(status=status.HTTP_200_OK)
