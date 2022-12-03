from django.contrib.auth import get_user_model

from rest_framework import serializers

from posts.models import Post
from posts.usecases import get_posts_with_optimization

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for short information about user"""

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]

    def get_followers_count(self, obj) -> int:
        return obj.followers.count()

    def get_following_count(self, obj) -> int:
        return obj.following.count()


class UserPostSerializer(serializers.ModelSerializer):
    """Duplicate serializer for Post model to avoid circular import from posts app"""

    content = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "content", "created_at", "updated_at", "image",
                  "likes_count", "comments_count"]

    def get_content(self, obj) -> str:
        return obj.content[:80]

    def get_image(self, obj) -> str | None:
        img = obj.images.all()[:1]
        if img:
            return img[0].image.url
        return None

    def get_likes_count(self, obj) -> int:
        return obj.likes.count()

    def get_comments_count(self, obj) -> int:
        return obj.comments.count()


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user with all fields and posts"""

    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)
    posts = UserPostSerializer(many=True, read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "avatar", "email", "posts_count",
                  "followers_count", "following_count", "is_following", "posts"]

    def get_is_following(self, obj) -> bool:
        user = self.context["request"].user
        if user.is_authenticated:
            if obj in user.following.all():
                return True
        return False


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "avatar"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
