from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from ..serializers import (
    UserRegistrationSerializer,
    UserActivationSerializer
)

User = get_user_model()


class RegistrationAPIView(APIView):
    """View for registration user"""

    @extend_schema(request=UserRegistrationSerializer, responses=None)
    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.create(serializer.validated_data)

        return Response(
            "New user was created. Confirmation link sent to email.",
            status=status.HTTP_201_CREATED,
        )


class UserActivateAPIView(APIView):
    """View for activate new user with code from email"""

    @extend_schema(request=UserActivationSerializer, responses=None)
    def post(self, request):
        data = request.data

        serializer = UserActivationSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.activate_user()

        return Response("Account successfully activated", status=status.HTTP_200_OK)
