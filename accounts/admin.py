from django.contrib import admin

from .models import UserFollowing, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active']

admin.site.register(UserFollowing)
