from django.contrib import admin
from .models import BlogModel, Tag, Comment, Reply

# Register your models here.

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]

admin.site.register(BlogModel)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
