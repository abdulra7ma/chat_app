from concurrent.futures import thread

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from .models import Chat, Message

User = get_user_model()


def get_last_10_messages(thread_id):
    chat = get_object_or_404(Chat, id=thread_id)
    print(Message.objects.filter(thread=chat))
    return Message.objects.filter(thread=chat)


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return Chat.objects.get(users__in=[user])


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
