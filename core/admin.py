import datetime

from django.contrib import admin
from django.utils import timezone

from core.models import Comment, Post, Profile

admin.site.register(Profile)
admin.site.register(Comment)


def delete_very_old_posts(modeladmin, request, queryset):
    queryset.filter(date_pub__lte=timezone.now() - datetime.timedelta(weeks=48)).delete()


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'image']}),
        ('Detail information', {'fields': ['description', 'get_likes']}),
        ('Date information', {'fields': ['date_pub', 'date_edit']}),
    ]
    readonly_fields = ['get_likes', 'date_pub', 'date_edit']
    list_display = ('author', 'date_pub', 'date_edit', 'published')
    list_filter = ('date_pub', 'date_edit')
    search_fields = ['author', 'description']
    actions = [delete_very_old_posts, 'make_pub_now']

    @staticmethod
    def make_pub_now(modeladmin, request, queryset):
        queryset.update(date_pub=timezone.now(), date_edit=timezone.now())


admin.site.register(Post, PostAdmin)

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class PostInline(admin.TabularInline):
    model = Post
    fields = ['author', 'image', 'description', 'get_likes', 'date_pub', 'date_edit']
    readonly_fields = ['get_likes', 'date_pub', 'date_edit']
    extra = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [PostInline]


