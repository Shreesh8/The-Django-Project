from django.urls import re_path, path
from . import views
from .views import BlogListPosts, PostActions

app_name = "post"

blog = BlogListPosts()
post_actions = PostActions()

urlpatterns = [
    # Misc
    path("about/", views.Info.about_us, name = "about"),
    path("contact/", views.Info.contact_us, name = "contact"),

    # Posts
    path("index/", blog.list_posts, name = "index"),
    re_path(r'^(?P<id>\d+)/$', views.post_detail, name = "detail"), 
    # r'^(?P<id>\d+)/$' doesnt work with path
    path("create/", views.post_create, name = "create"),

    # Post actions
    re_path(r'^(?P<id>\d+)/update/$', views.post_update, name = "update"),
    re_path(r'^(?P<id>\d+)/delete/$', views.post_delete, name = "delete"),
    re_path(r'^(?P<id>\d+)/report/$', views.post_report, name = "report"),

    re_path(r'^(?P<id>\d+)/upvote/$', post_actions.upvote_in_blog, name = "upvote_post"),
    re_path(r'^(?P<id>\d+)/upvote/detail/$', post_actions.upvote_in_detail, name = "upvote_post_detail"),
]
