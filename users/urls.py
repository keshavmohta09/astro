from django.urls import path
from rest_framework.authtoken import views as auth_views

from users import views

urlpatterns = [
    path("create/", views.UserAPI().create, name="user-create"),
    # path("update/", views.UserAPI.as_view({"put": "update"}), name="user-update"),
    path(
        "login/",
        views.UserAuthenticationAPI().login,
        name="user-login",
    ),
    path(
        "logout/",
        views.UserAuthenticationAPI.as_view({"delete": "logout"}),
        name="user-logout",
    ),
]
