from chat.models import Message as Messages_model
from rest_framework import serializers
from api.accounts.serializers import UserPublicSerializers


class MessagesSerializer(serializers.ModelSerializer):
    sender = UserPublicSerializers(read_only=True)

    class Meta:
        model = Messages_model
        fields = "__all__"

