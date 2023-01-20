from rest_framework import fields, serializers
from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer
from .models import Chat, Message
from userprofile.serializers import UserInfoChat


class ChatSerializer(serializers.ModelSerializer):
    
    user1 = UserInfoChat(read_only=True)
    user2 = UserInfoChat(read_only=True)
    last_msg = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Chat
        fields = ["id","user1","user2", "last_msg"] 
        
    def get_last_msg(self, obj):
        return last_message(obj)
         
   
class ChatUserListSerializer(serializers.ModelSerializer):
    
    user= UserInfoChat(read_only=True)
    last_msg = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Message
        fields = ["id", "user","last_msg","date"]
        order = "-date"
        
    
    def get_last_msg(self, obj):
        return last_message(obj)
    
    
class MessageSerializer(serializers.ModelSerializer):
    
    user= UserInfoChat(read_only=True)
    
    class Meta:
        model = Message
        fields = ["id", "user","text","date"]
        
     
def last_message(obj):
    msg = obj.last_msg()
    serialzer = MessageSerializer(msg)
    return serialzer


        
    
    

        
    