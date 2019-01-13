from functools import partial

from django.contrib import admin
from django.urls import path, include
from django.views.defaults import permission_denied

from . import user_urls
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/change_password', views.PasswordChangeView.as_view(), name="change_password"),
    path('accounts/signup', views.signup, name="register"),
    path("", views.PostsView.as_view(), name="index"),
    path('accounts/', include('django.contrib.auth.urls',)),
    path('profile/', include(user_urls)),
    path('content/', include('content.urls'))
]

handler403 = partial(permission_denied, template_name="shared/no_permission.html")
