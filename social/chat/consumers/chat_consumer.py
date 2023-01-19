import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .db_usecases import (
    create_new_message,
    get_message_recipient,
    get_user_by_pk,
    make_message_read,
)


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer for receive and send messages"""

    async def connect(self):
        self.group_name = str(self.scope["user"].pk)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def handle_action(self, action_type, data):
        if action_type == "send_message":
            message = data["message"]
            user = self.scope["user"]
            send_to = data["send_to"]

            if user.pk == send_to:
                return ""
            await self.channel_layer.group_send(
                str(send_to),
                {
                    "type": "send_message",
                    "username": user.username,
                    "message": message,
                },
            )

            recipient = await get_user_by_pk(send_to)

            if not recipient:
                return "There is no user"

            else:
                await create_new_message(user, recipient, message)

        elif action_type == "read_message":
            message_id = data["message_id"]
            user = self.scope["user"]
            recipient = await get_message_recipient(message_id)
            if recipient:
                if recipient == user:
                    await make_message_read(message_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if not ("type" in text_data_json):
            await self.send(text_data="action type should be set")
        else:
            await self.handle_action(text_data_json["type"], text_data_json)

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )
