import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .db_usecases import create_new_message, get_user_by_pk
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = str(self.scope['user'].pk)
        await self.channel_layer.group_add(
            self.group_name ,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.group_name ,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        send_to = text_data_json['send_to']
        
        if user.pk == send_to:
            return "User can't send message himself"

        await self.channel_layer.group_send(
            str(send_to),{
                "type" : "send_message",
                "username": user.username,
                "message" : message,
            })
        recipient = await get_user_by_pk(send_to)

        if not recipient:
            return "There is no user"
        else:
            await create_new_message(user, recipient, message)

    async def send_message(self, event) :
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))