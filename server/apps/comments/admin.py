from django.contrib import admin

from apps.comments.models.comment import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'profile', 'content', 'created', 'content_type', 'object_id', 'content_object',
    )
