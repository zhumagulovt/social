from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.settings import api_settings

from accounts.models import UserFollowing
from posts.models import Post
from posts.usecases import get_posts_with_optimization

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'email',
            'followers_count',
            'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
    
    def validate(self, data):
 
        user = User(**data)
        password = data.get('password')

        # password validation
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        return user


class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, data):
        # check base64 uid and decode it to user id
        try:
            uid = force_str(urlsafe_base64_decode(data.get('uid')))

            # change base64 encoded uid to normal user id, to use it in views
            data['uid'] = uid

            user = User.objects.get(pk=uid)
        except BaseException as e:
            raise ValidationError("Invalid uid")

        if not default_token_generator.check_token(user=user, token=data.get('token')):
            raise serializers.ValidationError({"token": "Invalid token"})

        return data

    def activate_user(self):
        user = User.objects.get(pk=self.data.get('uid'))
        user.is_active = True

        # to make used token invalid
        user.last_login = timezone.now()
        
        user.save()


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        user = self.context.get('user')
        
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Current password is invalid"}
            )
        
        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "New password is similar to current"}
            )
        
        # password validation
        try:
            validate_password(new_password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"new_password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return data


class UserResetPasswordSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)

    def validate(self, data):

        if not User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                {"email": "Invalid email"}
            )

        return data


class UserResetPasswordCompleteSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):

        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # decode base64 encoded uid to user id
        try:
            uid = force_str(urlsafe_base64_decode(data.get('uid')))
 
            user = User.objects.get(pk=uid)

            # add the user to data, whose password needs to be reset
            # we need to get user in views
            data['user'] = user

        except BaseException as e:
            raise ValidationError("Invalid uid")

        if not default_token_generator.check_token(user=user, token=data.get('token')):
            raise serializers.ValidationError({"token": "Invalid token"})

        # password validation
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        
        # password confirm validation
        if password != password_confirm:
            raise serializers.ValidationError({"passwords aren't match"})

        return data


class UserPostSerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
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


class UserDetailSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'email',
            'posts_count',
            'followers_count',
            'following_count',
            'is_following',
            'posts'
        ]

    def get_posts(self, obj):
        queryset = get_posts_with_optimization(user=obj)
        return UserPostSerializer(queryset, many=True).data

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_is_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if UserFollowing.objects.filter(user=user,following=obj).exists():
                return True
        return False

    def get_posts_count(self, obj):
        return obj.posts.count()


class UserEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'avatar'
        ]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)