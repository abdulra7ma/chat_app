from django.urls import path

from . import views

urlpatterns = [
    path("", views.chatroom, name="chatroom"),
    path("m/<str:username>/", views.ThreadView.as_view(), name="one-chatroom"),
]
