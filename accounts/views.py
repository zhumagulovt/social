from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import send_confirmation_link
from .serializers import *
from .models import UserFollowing

User = get_user_model()


class RegistrationAPIView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            
            return Response(
                "New user was created. Confirmation link sent to email.",
                status=status.HTTP_201_CREATED
            )


class UserActivateAPIView(APIView):
    
    def post(self, request):
        data = request.data
        
        serializer = UserActivationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.activate_user()

            return Response(
                "Account successfully activated",
                status=status.HTTP_200_OK
            )


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


class UserDetailView(generics.RetrieveAPIView):
    lookup_field = "username"
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserEditView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer

    def get_object(self):
        return self.request.user


class UserDeleteAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.avatar = "avatars/default.jpg"
        user.save()
        return Response(status=status.HTTP_200_OK)


    # def patch(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)


# class UserEditView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
    
#     def update(self, request):
#         user = request.user
#         serializer = UserEditSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()


class UserFollowView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user = request.user
        to_follow = User.objects.get(username=username)

        if user == to_follow:
            return Response("User can't follow himself", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if UserFollowing.objects.filter(user=user, following=to_follow).exists():
            # unfollow
            UserFollowing.objects.filter(user=user, following=to_follow).delete()
        else:
            # follow
            UserFollowing.objects.create(user=user, following=to_follow)

        return Response(status=status.HTTP_200_OK)


class UserFollowingListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        queryset = User.objects.filter(followers__user=user)
        return queryset


class UserFollowerListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        
        user = User.objects.get(username=self.kwargs.get('username'))
        # in models user's related name is following
        queryset = User.objects.filter(following__following=user)
        return queryset
