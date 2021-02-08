from django.core.management.base import BaseCommand
from message.factories import MessageFactory

class Command(BaseCommand):
    help = "Generate some random Message objects"

    def add_arguments(self, parser):
        parser.add_argument("nr_messages", type=int)

    def handle(self, *args, **options):
        n = options["nr_messages"]
        MessageFactory.create_batch(n)
