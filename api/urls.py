from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("accounts/", include("api.accounts.urls", namespace="accounts-api")),
    path("chat/", include("api.chat.urls", namespace="chat-api")),
]
