import pytest
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
class NewMessagesTest:
    def test_no_new_messages(self, api_client):
        response = api_client.get(reverse("message:list_new"))
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.freeze_time
    def test_single_new_message(self, api_client, message):
        assert message.retrieved_at is None
        response = api_client.get(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data

        assert len(data) == 1
        message_json = data[0]
        assert message_json["content"] == message.content
        assert message_json["recipient"] == message.recipient.username

        # Message in DB should now be marked as seen
        message.refresh_from_db()
        assert message.retrieved_at == timezone.now()

    def test_multiple_new_messages(self, api_client, message_factory):
        messages = message_factory.create_batch(2)
        messages.sort(key=lambda m: m.created_at, reverse=True)
        response = api_client.get(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data

        assert len(data) == 2
        # Most recent message should be first
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2

    def test_retrieve_twice(self, api_client, message_factory):
        message_factory.create()

        response = api_client.get(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data
        assert len(data) == 1

        # Message should only be retrieved once
        response = api_client.get(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data
        assert len(data) == 0
