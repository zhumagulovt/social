from rest_framework.generics import ListAPIView, CreateAPIView, \
    DestroyAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly


class FollowingFeedView(ListAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = PostsListSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(
            user__followers__user=user
        )
        return queryset


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()


class PostDetailDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)
        
        return Response(status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data
        data['post'] = pk
        data['user'] = request.user.pk
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

        if Saved.objects.filter(user=user, post=post).exists():
            Saved.objects.filter(user=user, post=post).delete()
        else:
            Saved.objects.create(user=user, post=post)
        
        return Response(status=status.HTTP_200_OK)


class UserSavedList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(
            saved__user=user
        )
        return queryset