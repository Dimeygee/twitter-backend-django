from notifications.models import Notification
from rest_framework import  serializers
from users.serializers import UserSerializer
from tweets.serializers import NotTweetSerializer



class NotifcationSerializer(serializers.ModelSerializer):
    
    from_user = UserSerializer(read_only=True)
    tweet = NotTweetSerializer(read_only=True)
    to_user = serializers.CharField(source="to_user.username")
    
    class Meta: 
        model = Notification
        fields = "__all__"
        

   
