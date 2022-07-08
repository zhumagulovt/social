from django.urls import path

from . import views

urlpatterns = [

    path('', views.FollowingFeedView.as_view()),
    path('<int:pk>/', views.PostDetailDeleteView.as_view()),
    path('<int:pk>/add_comment/', views.CommentCreateView.as_view()),
    path('<int:pk>/like/', views.LikeView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('comment/<int:pk>/', views.CommentDeleteView.as_view())
]