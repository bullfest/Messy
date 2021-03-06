import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import Message


@pytest.mark.django_db
class CreateMessageTest:
    def test_create_message(self, api_client):
        recipient = "king_arthur"
        content = "I fart in your general direction!"

        response = api_client.post(
            reverse("message:create"),
            {
                "recipient": recipient,
                "content": content,
            },
        )
        assert response.status_code == 200
        data = response.data
        assert data["id"] == 1
        assert data["recipient"] == recipient
        assert data["content"] == content
        assert data["retrieved_at"] is None

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.content == content
        assert message.recipient.username == recipient

    def test_extra_fields_ignored(self, api_client):
        response = api_client.post(
            reverse("message:create"),
            {
                "recipient": "king_arthur",
                "content": "Listen -- Strange women lying in ponds "
                "distributing swords is no basis "
                "for a system of government.",
                "created_at": "2020-12-24T15:00+01:00",
            },
        )
        assert response.status_code == 200
        message = Message.objects.first()
        assert message
        assert message.created_at - timezone.now() < timezone.timedelta(minutes=5)

    def test_required_fields(self, api_client):
        response = api_client.post(reverse("message:create"))

        assert response.status_code == 400
        assert set(response.data.keys()) == {"recipient", "content"}


@pytest.mark.django_db
class NewMessagesTest:
    def test_no_new_messages(self, api_client):
        response = api_client.post(reverse("message:list_new"))
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.freeze_time
    def test_single_new_message(self, api_client, message):
        assert message.retrieved_at is None
        response = api_client.post(reverse("message:list_new"))
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
        response = api_client.post(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data

        assert len(data) == 2
        # Most recent message should be first
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2

    def test_retrieve_twice(self, api_client, message_factory):
        message_factory.create()

        response = api_client.post(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data
        assert len(data) == 1

        # Message should only be retrieved once
        response = api_client.post(reverse("message:list_new"))
        assert response.status_code == 200
        data = response.data
        assert len(data) == 0


@pytest.mark.django_db
class MessageDetailsViewTest:
    def test_get_missing_message(self, api_client):
        response = api_client.get(reverse("message:detail", kwargs={"id": 1}))
        assert response.status_code == 404

    def test_get_message(self, api_client, message):
        response = api_client.get(reverse("message:detail", kwargs={"id": message.id}))
        assert response.status_code == 200
        assert response.data["id"] == message.id

    def test_delete_message(self, api_client, message):
        assert Message.objects.count() == 1

        response = api_client.delete(
            reverse("message:detail", kwargs={"id": message.id})
        )
        assert response.status_code == 200
        assert response.data["id"] is None
        assert Message.objects.count() == 0


@pytest.mark.django_db
class MessageRangeViewTest:
    def test_no_matching_elements(self, api_client, message_factory):
        message_factory.create_batch(5)
        Message.objects.filter(id__in=(2, 3)).delete()
        response = api_client.get(
            reverse("message:range", kwargs={"begin_id": 2, "end_id": 3})
        )

        assert response.status_code == 200
        data = response.data
        assert len(data) == 0

    def test_single_element(self, api_client, message_factory):
        message_factory.create_batch(3)
        response = api_client.get(
            reverse("message:range", kwargs={"begin_id": 2, "end_id": 2})
        )

        assert response.status_code == 200
        data = response.data
        assert len(data) == 1
        assert data[0]["id"] == 2

    def test_out_of_bounds_range(self, api_client, message_factory):
        message_factory.create_batch(3)
        response = api_client.get(
            reverse("message:range", kwargs={"begin_id": 2, "end_id": 100})
        )

        assert response.status_code == 200
        data = response.data
        assert len(data) == 2
        assert data[0]["id"] == 2
        assert data[1]["id"] == 3


@pytest.mark.django_db
def test_full_flow(api_client):
    response = api_client.post(
        reverse("message:create"),
        {
            "recipient": "wensleydale",
            "content": "It's not much of a cheese shop is it?",
        },
    )
    assert response.status_code == 200

    response = api_client.post(
        reverse("message:create"),
        {
            "sender": "wensleydale",
            "recipient": "customer",
            "content": "Finest in the district!",
        },
    )
    assert response.status_code == 200

    response = api_client.post(reverse("message:list_new"))
    assert response.status_code == 200
    assert len(response.data) == 2

    response = api_client.post(reverse("message:list_new"))
    assert response.status_code == 200
    assert len(response.data) == 0

    response = api_client.post(
        reverse("message:create"),
        {
            "sender": "customer",
            "recipient": "wensleydale",
            "content": "Explain the logic underlying that conclusion, please.",
        },
    )

    response = api_client.post(reverse("message:list_new"))
    assert response.status_code == 200
    assert len(response.data) == 1

    response = api_client.delete(reverse("message:detail", kwargs={"id": 2}))
    assert response.status_code == 200
    response = api_client.get(
        reverse("message:range", kwargs={"begin_id": 1, "end_id": 3})
    )
    assert response.status_code == 200
    data = response.data
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 3

    wensleydale = User.objects.get(username="wensleydale")
    customer = User.objects.get(username="customer")
    assert wensleydale.sent_messages.count() == 0
    assert wensleydale.recieved_messages.count() == 2
    assert customer.sent_messages.count() == 1
    assert customer.recieved_messages.count() == 0
