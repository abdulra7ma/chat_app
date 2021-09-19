from django.contrib import admin
from django.urls import include, path

from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("messanger/", views.chatroom, name="chatroom"),
    path("messanger/<str:username>/", views.ThreadView.as_view(), name="one-chatroom"),
]
