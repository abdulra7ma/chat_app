from django.urls import path

from .views import MessagesAPIView

app_name = "chat-api"

urlpatterns = [path("messages", MessagesAPIView.as_view(), name="messages-api")]
