from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.chatroom, name="chatroom"),
    path("m/<str:username>/", views.ThreadView.as_view(), name="one-chatroom"),
    path("accounts/", include("account.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
