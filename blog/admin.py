from django.contrib import admin
from .models import *

#admin.site.register(Post)
#admin.site.register(Comment)

admin.site.register(Tag)

# With the help of CommentInline, which subclasses admin.StackedInline, 
# the comments can be displayed and edited inline with the Post they belong to
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'is_active','created_on')
    list_filter = ("is_active",)
    search_fields = ['headline', 'content']
    prepopulated_fields = {'slug': ('headline',)}
    inlines = [
        CommentInline,
    ]

admin.site.register(Post, PostAdmin)