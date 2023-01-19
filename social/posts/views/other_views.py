from rest_framework.generics import DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

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


class CommentCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get("pk")
        )


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
