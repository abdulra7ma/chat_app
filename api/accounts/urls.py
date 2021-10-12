from django.urls import include, path
from .views import AccountsAPIView


app_name = "accounts-api"

urlpatterns = [
    path("", AccountsAPIView.as_view(), name="accounts-api"),
]
