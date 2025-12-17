from django.contrib import admin
from .models import Post , Comment
# from admin_panel.models import ContactInfo
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','date']
    list_display_links = ['title','date'] 

    list_filter = ['date']
    search_fields = ['title']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
#admin.site.register(Comment, CommentAdmin)