import rest_framework.fields
from django.contrib.auth.models import User
from rest_framework import serializers

from message.models import Message


class UserAsUsernameField(rest_framework.fields.CharField):
    def to_representation(self, user: User):
        return user.username

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        user, __ = User.objects.get_or_create(username=value)
        return user


class MessageSerializer(serializers.ModelSerializer):
    recipient = UserAsUsernameField()

    class Meta:
        model = Message
        fields = [
            "content",
            "created_at",
            "id",
            "retrieved_at",
            "recipient",
        ]
        read_only_fields = [
            "retrieved_at",
        ]
