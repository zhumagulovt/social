from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        user = self.context.get("user")

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

        if not User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError({"email": "Invalid email"})

        return data


class UserResetPasswordCompleteSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):

        password = data.get("password")
        password_confirm = data.get("password_confirm")

        # decode base64 encoded uid to user id
        try:
            uid = force_str(urlsafe_base64_decode(data.get("uid")))

            user = User.objects.get(pk=uid)

            # add the user to data, whose password needs to be reset
            # we need to get user in views
            data["user"] = user

        except BaseException as e:
            raise ValidationError("Invalid uid")

        if not default_token_generator.check_token(user=user, token=data.get("token")):
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
