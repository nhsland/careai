from django.contrib import admin
from .models import Discussion, Comment


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'get_discussion_title')


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Comment, CommentAdmin)
