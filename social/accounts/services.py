from django.db.models import Count
from django.contrib.auth import get_user_model

from rest_framework.generics import get_object_or_404

User = get_user_model()


def get_user_detail(username: str) -> User:
    """get User with count of posts, followers and followings"""
    queryset = (
        User.objects.
        annotate(
            posts_count=Count('posts'),
            followers_count=Count('followers'),
            following_count=Count('following')
        ).
        prefetch_related('posts', 'posts__likes', 'posts__images', 'posts__comments')
    )

    user = get_object_or_404(queryset, username=username)

    return user
