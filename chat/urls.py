from django.urls import path

from .views import ChatListAPIView, ChatDetailAPIView

urlpatterns = [
    path('list/', ChatListAPIView.as_view()),
    path('chat-with/<int:pk>/', ChatDetailAPIView.as_view())
]
