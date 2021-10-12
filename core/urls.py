from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

import debug_toolbar

from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat.urls")),
    path("accounts/", include("account.urls")),
    re_path(r"^api/v1/", include("api.urls", namespace="api")),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
