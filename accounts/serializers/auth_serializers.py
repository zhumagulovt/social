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

User = get_user_model()


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
    """Serializer for activation user with uid and token"""
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
