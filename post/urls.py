from django.urls import re_path, path
from . import views

app_name = "post"

urlpatterns = [
    path("about/", views.about_us, name = "about"),
    path("contact/", views.contact_us, name = "contact"),

    path("index/", views.post_index, name = "index"),
    re_path(r'^(?P<id>\d+)/$', views.post_detail, name = "detail"), 
    # r'^(?P<id>\d+)/$' doesnt work with path
    path("create/", views.post_create, name = "create"),
    re_path(r'^(?P<id>\d+)/update/$', views.post_update, name = "update"),
    re_path(r'^(?P<id>\d+)/delete/$', views.post_delete, name = "delete"),
    re_path(r'^(?P<id>\d+)/upvote/$', views.upvote_post, name = "upvote_post"),
]
