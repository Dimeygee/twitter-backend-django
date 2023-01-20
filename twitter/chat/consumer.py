from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from .models import Chat, Message
from channels.db import database_sync_to_async
from notifications.models import Notification
from django.db.models  import Q



class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        
        await self.accept()
        
        self.me  = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["username"]
        self.user2 = await sync_to_async(User.objects.get)(username=self.other_username)
        self.private_room = await sync_to_async(Chat.objects.create_room_if_none)(self.me, self.user2)
        self.room_name = f"private_room_{self.private_room.id}"
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        
        
        
    async def receive_json(self,content):
        command = content.get("command", None)
        if command == "private_chat":
            message = content.get("message", None)

            self.newmsg = await sync_to_async(Message.objects.create)(
                chatroom=self.private_room,
                user=self.me,
                text=message
            )
            await self.message_notice()
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "websocket_message",
                    "text": message,
                    "id": self.newmsg.id,
                    "username": self.newmsg.user.username,
                    "profilephoto": self.newmsg.user.profilephoto.url,
                    "command": command
                }
            )
            
        if command == "is_typing":
            print('typing')
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "websocket_typing",
                    "text": content["text"],
                    "command": command,
                    "user": content["user"]
                }
            )
            
    async def websocket_message(self, event):

        await self.send_json(({
            'id': event["id"],
            'text': event["text"],
            'command': event["command"],
            'user': {
                "username": event["username"],
                "profilephoto": event["profilephoto"],
            }
        }))

    async def websocket_typing(self, event):
        await self.send_json((
            {
                'text': event["text"],
                'command': event["command"],
                'user': event["user"]
            }
        ))

    
    @database_sync_to_async
    def message_notice(self):
        if not Notification.objects.filter(Q(notification_type='M',to_user=self.user2,from_user=self.me) |  Q       (notification_type='M',to_user=self.me,from_user=self.user2)).exists():
            Notification.objects.create(notification_type='M',to_user=self.user2,from_user=self.me)

    async def disconnect(self, close_code):
        
        print("disconnected")
        
        await self.delete_room_if_no_chat_messages(self.me, self.user2)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        
    @database_sync_to_async
    def delete_room_if_no_chat_messages(self, me, user2):
        chat = Chat.objects.get(Q(user1=me, user2=user2) | Q(user1=user2, user2=me))
        if not chat.message:
            print("deleted")
            chat.objects.delete()
            
            
            
        
        
