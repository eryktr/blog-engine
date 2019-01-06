from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.show_profile, name="show_profile"),
]

