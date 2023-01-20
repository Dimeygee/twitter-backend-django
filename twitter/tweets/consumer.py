from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TwitterConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        user = self.scope.get("user")
        
        
        self.me = user.username
        
        await self.accept()
        
        print(user)
        
        self.room_name = f"Hi_{self.me}"
        self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        ) 
    
    async def receive_json(self, content):
        print("recieved message")
        message = content.get("message", None)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket_message",
                "text": message
           }
        )
    
    async def send_status(self,event):
        await self.send_json({ "payload": event })
        
    async def websocket_message(self, event):

        await self.send_json(({
            'message': event["text"],
            'user': self.me
        }))
    
    async def disconnect(self, close):
        print("disconnected")
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )