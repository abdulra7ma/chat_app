from rest_framework import generics
from .serializers import MessagesSerializer
from chat.models import Message
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from .filters import ThreadUserFilter

from django_auto_prefetching import AutoPrefetchViewSetMixin


class MessagesAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = MessagesSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ThreadUserFilter
    queryset = Message.objects.all()

    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        if not query.exists():
            content = {'message': "No Content"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return super().get(request, *args, **kwargs)
