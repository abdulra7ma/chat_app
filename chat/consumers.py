import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Chat, Message

User = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chatroom_message",
                "message": message,
                "username": username,
            },
        )

    async def chatroom_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )


class MessengerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = False

    @database_sync_to_async
    def get_user_username(self, id):
        user = User.objects.get(id=id)
        return user.username

    @database_sync_to_async
    def get_last_10_messages(self, thread_id):
        chat = get_object_or_404(Chat, id=thread_id)
        return Message.objects.filter(Q(thread=chat))

    async def new_message(self, *args, **kwargs):
        message = kwargs["data"]["message"]
        user = kwargs["user"]
        message = await sync_to_async(Message.objects.create)(
            thread=self.thread_obj, sender=user, message_content=message
        )
        content = {"command": "new_message", "message": self.message_to_json(message)}
        await self.send_message(content)

    @database_sync_to_async
    def _get_user(self, username):
        return User.objects.get(username=username)

    async def fetch_messages(self, **data):
        scope_user = data["user"].username
        messages = await self.get_last_10_messages(self.thread_obj.id)
        content = {
            "command": "messages",
            "messages": await sync_to_async(self.messages_to_json)(messages),
            "sender": scope_user,
        }
        await self.send_message(content)

    async def client_disconnect_status(self, *args, **kwargs):
        self._status = False

    commands = {
        "get_user_name": get_user_username,
        "new_message": new_message,
        "fetch_messages": fetch_messages,
        "disconnect": client_disconnect_status,
    }

    async def connect(self):
        user_id = self.scope["url_route"]["kwargs"]["username"]

        sender = self.scope["user"]
        reciever = await self._get_user(user_id)

        self.thread_obj = await sync_to_async(
            Chat.objects.get_or_create_personal_thread
        )(user1=sender, user2=reciever)

        self.room_name = f"personal_thread_{self.thread_obj.id}"
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        self._status = False
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        kwargs = {"user": self.scope["user"], "data": data}

        await self.commands[data["command"]](self, **kwargs)

        if data["command"] == "fetch_messages":
            self._status = True

    async def send_message(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chatroom_message", "message": data},
        )

    async def chatroom_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    def message_to_json(self, message):
        return {
            "id": message.id,
            "author": message.sender.username,
            "content": message.message_content,
            "timestamp": str(message.created_at),
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
