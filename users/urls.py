from django.contrib import messages
from django.shortcuts import render
from django.urls import path

from users import views
from users.models import UserQuery


def create_query(request):
    data = request.POST
    u = UserQuery(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        query=data["message"],
    )
    try:
        u.save()
    except Exception as error:
        messages.error(str(error))
        return render(request, "contact.html")
    return render(request, "index.html")


urlpatterns = [
    path("create/", views.UserAPI().create, name="user-create"),
    path("login/", views.UserAuthenticationAPI().login, name="user-login"),
    path("logout/", views.UserAuthenticationAPI().logout, name="user-logout"),
    path("query/", create_query, name="user-query"),
]
