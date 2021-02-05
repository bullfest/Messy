from django.db import transaction
from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


@api_view(http_method_names=["GET"])
def new_messages(request):
    with transaction.atomic():
        messages = list(
            Message.objects.filter(retrieved_at__isnull=True).order_by("created_at")
        )
        message_ids = (m.id for m in messages)
        Message.objects.filter(id__in=message_ids).update(retrieved_at=timezone.now())
        data = MessageSerializer(messages, many=True).data
        return Response(data)
