from django.contrib import admin

from .models import Message, Chat

admin.site.register(Chat)
admin.site.register(Message)
