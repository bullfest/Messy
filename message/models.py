import uuid
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """
    A message being sent from one user to another.
    """

    sender = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recieved_messages"
    )
    retrieved_at = models.DateTimeField(null=True, default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
