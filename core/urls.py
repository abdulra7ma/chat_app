from django.contrib import admin
from django.urls import include, path

from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.chatroom, name="chatroom"),
    path("m/<str:username>/", views.ThreadView.as_view(), name="one-chatroom"),
    path("accounts/", include("account.urls")),
]
