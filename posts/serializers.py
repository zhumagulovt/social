from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import *


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = "__all__"


class PostsListSerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'user',
            'created_at',
            'updated_at',
            'image',
            'likes_count',
            'comments_count'
        ]
    
    def get_content(self, obj):      
        return obj.content[:80]

    def get_image(self, obj):
        img = obj.images.all()[:1]
        if img:
            return img[0].image.url
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


class PostDetailSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)    
    images = PostImageSerializer(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'user',
            'created_at',
            'updated_at',
            'images',
            'likes_count',
            'comments_count',
            'comments'
        ]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()


class PostCreateSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'content',
            'images'
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        images_data = request.FILES
        post = Post.objects.create(**validated_data)

        for image in images_data.getlist('images'):
            PostImage.objects.create(post=post, image=image)

        return post


class CommentCreateSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'content'
        ]