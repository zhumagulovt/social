from django.contrib import admin

from .models import *

admin.site.register(PostImage)
admin.site.register(Comment)

class PostImageAdmin(admin.StackedInline):
    model = PostImage
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at', 'get_image']
    inlines = [PostImageAdmin]

    def get_image(self, obj):
        return ""
        return obj.images.all()[:1][0].image.url

    get_image.admin_order_field = "image"
    get_image.short_description = "First image"
    # list_display_links
