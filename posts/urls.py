from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostCreateView.as_view()),
    path("feed/", views.FollowingFeedView.as_view()),
    path("saved/", views.UserSavedList.as_view()),
    path("<int:pk>/", views.PostDetailDeleteView.as_view()),
    path("<int:pk>/add_comment/", views.CommentCreateView.as_view()),
    path("<int:pk>/like/", views.LikeView.as_view()),
    path("<int:pk>/save/", views.SavedView.as_view()),
    path("comment/<int:pk>/", views.CommentDeleteView.as_view()),
]
