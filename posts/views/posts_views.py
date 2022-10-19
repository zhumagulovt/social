from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from ..models import *
from ..serializers import *
from ..permissions import IsOwnerOrReadOnly
from ..usecases import get_posts_with_optimization


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000


class FollowingFeedView(ListAPIView):
    # permission_classes= [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = PostsListSerializer

    def get_queryset(self):
        # user = self.request.user
        user = User.objects.get(id=1)
        queryset = get_posts_with_optimization(user__followers=user)
        return queryset


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()


class PostDetailDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostDetailSerializer

    def get_object(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"]).prefetch_related(
            "comments__user__following", "comments__user__followers"
        )
        return queryset[0]


class UserSavedList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = get_posts_with_optimization(saved__user=user)
        return queryset

class PostSearch(ListAPIView):
    serializer_class = PostsListSerializer

    def get_queryset(self):
        q = self.request.query_params['q']
        if q != '':
            return get_posts_with_optimization(content__icontains=q)
        return []