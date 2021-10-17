from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from ..pagination import APICustomPagination
from .serializers import USER, UserPublicSerializers
from django.core.cache import cache


class AccountsAPIView(generics.ListAPIView):
    serializer_class = UserPublicSerializers
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    pagination_class = APICustomPagination

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        req_usr = self.request.user
        if req_usr.is_superuser:
            return USER.objects.all().prefetch_related("groups", "user_permissions")
        return USER.objects.filter(id=req_usr.id)
