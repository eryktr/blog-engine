from django.urls import path, include
from . import views

urlpatterns = [
    path("new_post/", views.new_post, name="newpost"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("view_post/<int:post_id>", views.view_post, name="view_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post")
]