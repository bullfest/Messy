from django.urls import path

from . import views

app_name = "message"
urlpatterns = [
    path("", views.create_message, name="create"),
    path("<int:id>/", views.message_detail, name="detail"),
    path("new/", views.new_messages, name="list_new"),
    path("range/<int:begin_id>/<int:end_id>/", views.message_range_view, name="range"),
]
