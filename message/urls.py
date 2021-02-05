from django.urls import path

from . import views

app_name = "message"
urlpatterns = [
    path("new/", views.new_messages, name="list_new"),
]
