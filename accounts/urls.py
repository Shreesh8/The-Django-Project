from django.urls import path, re_path, include
from . import views

app_name = "accounts"

urlpatterns = [

    # Main Account logic
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path("signin/", views.signin_view, name = "signin"),
]
