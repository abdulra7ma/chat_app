from django.contrib.auth import get_user_model
from rest_framework import serializers


USER = get_user_model()


class UserPublicSerializers(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = USER
        fields = ["id", "username", "email", "mobile", "uri"]

    def get_uri(self, obj):
        request = self.context.get("request")
        avatar_uri = obj.avatar.url
        return request.build_absolute_uri(avatar_uri)
