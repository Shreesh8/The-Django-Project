from django.urls import path

from . import views

app_name = "user_profile"

urlpatterns = [
    path('test/', views.test , name="test"),
]