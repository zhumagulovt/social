import json
from channels.generic.websocket import AsyncWebsocketConsumer
 
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
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        send_to = text_data_json['send_to']

        await self.channel_layer.group_send(
            str(send_to),{
                "type" : "send_message",
                "username": user.username,
                "message" : message,
            })

    async def send_message(self, event) :
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))