from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


@api_view(http_method_names=["POST"])
def create_message(request):
    """Create a new Message.

    Required data:
    recipient: Username of the recipient
    content: The content of the message

    Optional data:
    sender: Username of the sender
    """
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["POST"])
def new_messages(request):
    """Retrieve new messages that haven't been retrieved from this view before."""
    with transaction.atomic():
        messages = list(
            Message.objects.filter(retrieved_at__isnull=True).order_by("created_at")
        )
        message_ids = (m.id for m in messages)
        Message.objects.filter(id__in=message_ids).update(retrieved_at=timezone.now())
        data = MessageSerializer(messages, many=True).data
        return Response(data)


@api_view(http_method_names=["GET", "DELETE"])
def message_detail(request, id: int):
    """Detail view for Message objects.
    GET - Retrieve the Message with id
    DELETE - Delete the message with id, will also return the Message that's deleted
    """
    message = get_object_or_404(Message, id=id)
    if request.method == "DELETE":
        message.delete()
    return Response(MessageSerializer(message).data)


@api_view(http_method_names=["GET"])
def message_range_view(request, begin_id: int, end_id: int):
    """Retrieve a list of messages with id between (and including) begin_id and end_id."""
    messages = Message.objects.filter(id__gte=begin_id, id__lte=end_id).order_by(
        "created_at"
    )
    return Response(MessageSerializer(messages, many=True).data)
