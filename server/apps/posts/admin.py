from django.contrib import admin

from .models.posts import Post


@admin.register(Post)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created')
