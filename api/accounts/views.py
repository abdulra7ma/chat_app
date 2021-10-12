from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserPublicSerializers, USER


class AccountsAPIView(generics.ListAPIView):
    serializer_class = UserPublicSerializers
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        req_usr = self.request.user
        if req_usr.is_superuser:
            return USER.objects.all()
        return USER.objects.filter(id=req_usr.id)
