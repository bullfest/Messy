import pytest
from django.utils import timezone

from .models import Message
from .serializers import MessageSerializer


@pytest.mark.django_db
class TestMessageSerializer:
    def test_serialize(self, message):
        data = MessageSerializer(message).data
        assert set(data.keys()) == {
            "id",
            "content",
            "recipient",
            "sender",
            "created_at",
            "retrieved_at",
        }
        assert data["id"] == message.id
        assert data["content"] == message.content
        assert data["recipient"] == message.recipient.username

    @pytest.mark.freeze_time
    def test_deserialize(self):
        serializer = MessageSerializer(
            data={
                "recipient": "dr_gumby",
                "content": "My brain hurts!",
            }
        )
        serializer.is_valid()
        assert not serializer.errors
        serializer.save()
        message = Message.objects.first()
        assert message
        assert message.content == "My brain hurts!"
        assert message.recipient.username == "dr_gumby"
        assert message.created_at == timezone.now()
        assert message.retrieved_at is None
        assert message.sender is None
