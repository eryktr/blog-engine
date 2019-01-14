from django.urls import path

from . import views

urlpatterns = [
    path("new_post/", views.new_post, name="newpost"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    path("view_post/<int:post_id>", views.view_post, name="view_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("view_post/<int:post_id>/new_comment", views.new_comment, name="new_comment"),
    path("view_post/<int:post_id>/edit_comment/<int:comment_id>", views.edit_comment, name="edit_comment"),
    path("view_post/<int:post_id>/delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
]