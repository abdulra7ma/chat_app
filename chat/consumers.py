import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404

from account.models import Friends, Account

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
    @database_sync_to_async
    def get_user_username(self, id):
        user = User.objects.get(id=id)
        return user.username

    @database_sync_to_async
    def get_last_10_messages(self, thread_id):
        chat = get_object_or_404(Chat, id=thread_id)
        return Message.objects.filter(Q(thread=chat))

    @database_sync_to_async
    def _get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def check_freind(self, user_id):
        user = self.scope["user"]
        friend_obj = Friends.objects.filter(user=user)

        if not friend_obj.exists():
            Friends.objects.create(user=user)
            return False

        friend_obj = friend_obj.first()
        friends_ids = friend_obj.friends.all().values_list("id", flat=True)

        if user_id in list(friends_ids):
            return True

        return False

    async def new_message(self, *args, **kwargs):
        message = kwargs["data"]["message"]
        user = await sync_to_async(Account.objects.get)(id=kwargs["data"]["sender_id"])
        reciever_id = kwargs["data"]["reciever_id"]

        if not await self.check_freind(reciever_id):
            reciever_obj = await sync_to_async(Account.objects.get)(id=reciever_id)
            user = await sync_to_async(Friends.objects.get)(user=user)
            await sync_to_async(user.add_friend)(reciever_obj)

        message = await sync_to_async(Message.objects.create)(
            thread=self.thread_obj, sender=self.scope["user"], message_content=message
        )
        content = {"command": "new_message", "message": self.message_to_json(message)}
        await self.send_message(content)

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


class SearchConsumer(AsyncWebsocketConsumer):
    room_group_name: str
    room_name: str

    @staticmethod
    def user_to_json(user):
        print(user)
        return {"id": user[0], "username": user[1], "avatar_url": user[2]}

    @database_sync_to_async
    def get_10_user(self, username):
        users = User.objects.filter(Q(username__startswith=username))[:5].values_list(
            "id", "username", "avatar"
        )
        return users

    async def connect(self):
        self.room_name = f"{self.scope['user'].id}"
        self.room_group_name = "thread_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "search":
            if data["input"] != "":
                users = await self.get_10_user(data["input"])
                user_json = await sync_to_async(self.users_to_json)(users)
                await self.send_event(user_json)

    async def send_event(self, data):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "users_send", "data": data}
        )

    async def users_send(self, event):
        await self.send(text_data=event["data"])

    def users_to_json(self, users):
        result = []
        for user in users:
            result.append(self.user_to_json(user))

        return json.dumps(result)
