from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_profile, name="show_profile"),
    path('posts', views.UserPostsView.as_view(), name="show_user_posts")
]

