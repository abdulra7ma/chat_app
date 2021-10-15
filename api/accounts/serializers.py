from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class UserPublicSerializers(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    last_login = serializers.CharField(source="updated")

    class Meta:
        model = USER
        fields = [
            "id",
            "email",
            "username",
            "mobile",
            "is_active",
            "is_staff",
            "last_login",
            "uri",
        ]

    def get_uri(self, obj):
        request = self.context.get("request")
        avatar_uri = obj.avatar.url
        return request.build_absolute_uri(avatar_uri)


class UserPublicForMessagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["id", "username"]
