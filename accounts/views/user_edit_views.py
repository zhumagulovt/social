from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..utils import send_confirmation_link
from ..serializers import *

User = get_user_model()


class UserChangePasswordAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = UserChangePasswordSerializer(data=data, context={"user": user})

        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()

            return Response(
                "Password was changed",
                status=status.HTTP_200_OK
            )


class UserResetPasswordAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserResetPasswordSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            send_confirmation_link(
                "accounts/reset_password_mail.html", user, "Reset password"
            )

            return Response(
                "Link to reset was sent to email",
                status=status.HTTP_200_OK
            )


class UserResetPasswordCompleteAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserResetPasswordCompleteSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            user.set_password(serializer.validated_data.get('password'))
            user.save()

            return Response(
                "Password has been reset",
                status=status.HTTP_200_OK
            )
