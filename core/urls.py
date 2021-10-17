import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from chat import views

schema_view = get_schema_view(
   openapi.Info(
      title="Chat API",
      default_version='v1',
      description="Chat api for consumers",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="7amda License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat.urls")),
    path("accounts/", include("account.urls")),
    re_path(r"^api/v1/", include("api.urls", namespace="api")),
    path("__debug__/", include(debug_toolbar.urls)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
