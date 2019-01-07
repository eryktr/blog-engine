from django.urls import path, include
from . import views

urlpatterns = [
    path("newpost/", views.new_post, name="newpost")
]