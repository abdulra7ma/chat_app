from rest_framework import serializers

from api.accounts.serializers import UserPublicForMessagesSerializers
from chat.models import Message as Messages_model


class MessagesSerializer(serializers.ModelSerializer):
    sender = UserPublicForMessagesSerializers(read_only=True)

    class Meta:
        model = Messages_model
        fields = "__all__"
