from django.contrib import admin

from .models.profile import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'img', 'bio', 'location')
    readonly_fields = ('user',)
