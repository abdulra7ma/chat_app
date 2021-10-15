from django_filters import rest_framework as filters

from chat.models import Message as MessagesModel


class ThreadUserFilter(filters.FilterSet):
    sender = filters.CharFilter(field_name="sender__username", lookup_expr="exact")

    class Meta:
        model = MessagesModel
        fields = ("thread", "sender", "is_read")
