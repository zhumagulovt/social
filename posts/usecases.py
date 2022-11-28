from django.contrib.auth import get_user_model
from django.db.models import Model, Count
from django.db.models.expressions import Exists

from .models import Post

User = get_user_model()


def get_posts_with_optimization(user, **kwargs):
    """Get posts with filter and optimize by all reverse fields"""
    queryset = (
        Post.objects.filter(**kwargs)
        .annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments'),
        )
        .select_related("user")
        .prefetch_related(
            "images", "comments", "likes", "saved", "user__following", "user__followers"
        )
    )
    return queryset


def delete_or_create_user_m2m_post_model(model: Model, user: User, post: Post) -> None:
    """Delete or create m2m model that makes relation between User and Post"""

    if model.objects.filter(user=user, post=post).exists():
        model.objects.filter(user=user, post=post).delete()
    else:
        model.objects.create(user=user, post=post)
