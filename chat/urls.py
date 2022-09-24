from django.urls import include, path

from .views import ChatListAPIView

urlpatterns = [
    path('list/', ChatListAPIView.as_view())
]
