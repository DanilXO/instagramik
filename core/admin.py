from django.contrib import admin

from core.models import Comment, Post, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
