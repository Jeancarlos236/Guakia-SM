from django.urls import path, re_path

from . import api
from . import consumers

urlpatterns = [
    path("", api.conversation_list, name="conversations_list"),
    path("<uuid:pk>/", api.conversation_detail, name="conversations_detail"),
    path("<uuid:pk>/send/", api.conversation_sent_message, name="conversations_sent_message"),
    path("<uuid:user_pk>/get-or-create/", api.conversation_get_or_create, name="conversations_get_or_create"),
]

