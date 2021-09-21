from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from .views import SignUp
from .forms import UserLoginForm

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="login.html", form_class=UserLoginForm, success_url="/"
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
]
