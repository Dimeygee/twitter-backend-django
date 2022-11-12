from django.db import models
from users.models import User
from django.db.models import Q

class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Message.objects.filter(chat=room).order_by("-date")
        return messages

class PrivateChatManager(models.Manager):
    def create_room_if_none(self,u1,u2):
        has_room = Chat.objects.filter(Q(user1=u1,user2=u2) | Q(user1=u2,user2=u1)).first()
        if not has_room:
            Chat.objects.create(user1=u1,user2=u2)
        return has_room
    
        

class Chat(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user2")
    
    objects = PrivateChatManager()
    
    def last_msg(self):
        return self.message_set.all().last()
    
    
class Message(models.Model):
    chatroom = models.ForeignKey(Chat,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    objects = MessageManager()