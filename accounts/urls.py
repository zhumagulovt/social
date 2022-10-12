from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("registration/", views.RegistrationAPIView.as_view()),
    path("activate/", views.UserActivateAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", views.UserChangePasswordAPIView.as_view()),
    path("reset-password/", views.UserResetPasswordAPIView.as_view()),
    path("reset-password/completed/", views.UserResetPasswordCompleteAPIView.as_view()),
    path("edit/", views.UserEditView.as_view()),
    path("delete-avatar/", views.UserDeleteAvatarView.as_view()),
    path("<slug:username>/", views.UserDetailView.as_view()),
    path("<slug:username>/follow/", views.UserFollowView.as_view()),
    path("<slug:username>/followings/", views.UserFollowingListView.as_view()),
    path("<slug:username>/followers/", views.UserFollowerListView.as_view()),
]
