from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from chat.models import Message

from ..pagination import APICustomPagination
from .filters import ThreadUserFilter
from .serializers import MessagesSerializer


class MessagesAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = MessagesSerializer
    filter_backends = (DjangoFilterBackend,)
    queryset = Message.objects.all()
    filterset_class = ThreadUserFilter
    pagination_class = APICustomPagination

    @method_decorator(cache_page(10))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
