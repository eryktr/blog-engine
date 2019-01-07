from django.contrib import admin
from django.urls import path, include
from . import views
from . import user_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/change_password', views.PasswordChangeView.as_view(), name="change_password"),
    path('accounts/signup', views.signup, name="register"),
    path("", views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls',)),
    path('profile/', include(user_urls)),
    path('content/', include('content.urls'))
]
