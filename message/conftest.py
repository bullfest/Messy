from .factories import UserFactory, MessageFactory
from pytest_factoryboy import register

register(UserFactory)
register(MessageFactory)
