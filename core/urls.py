from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat.urls")),
    path("accounts/", include("account.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
