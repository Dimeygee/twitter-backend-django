from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Tweets
from hastags.models import HashTag


class TweetSerialzer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username",read_only=True)
    name= serializers.CharField(source="user.name",read_only=True)
    email= serializers.CharField(source="user.email",read_only=True)
    coverphoto= serializers.SerializerMethodField()
    profilephoto= serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    replies_count= serializers.SerializerMethodField()
    likes_count= serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    retweet_count =serializers.SerializerMethodField()
    retweet = serializers.SerializerMethodField()

    class Meta:
        model=Tweets
        fields=['id','username','name','email','coverphoto','profilephoto','content',"image",'date_posted','replies_count','likes_count','replies','retweet_count', "retweet", "likes"]

    def get_replies_count(self, obj):
        return obj.get_children.count()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_retweet_count(self,obj):
        return obj.retweet.count()

    def get_retweet(self,obj):
        user = self.context.get("request").user
        if user in obj.retweet.all():
            return True
        return False 
    
    def get_likes(self, obj):
        user = self.context.get("request").user
        if user in obj.likes.all():
            return True
        return False
    
    def get_coverphoto(self,obj):
        return coverphoto(obj)

    def get_profilephoto(self,obj):
        return profilephoto(obj)


    def get_replies(self,obj):
        return replies(obj)

    def create(self,validated_data):
        tweet = Tweets.objects.create(**validated_data)

        words = validated_data['content'].split(" ")
        for word in words:
            if word[0] == "#":
                hastag, created = HashTag.objects.get_or_create(name=word[1:])
                hastag.tweet.add(tweet)

        return tweet

def replies(obj):
    replies = obj.get_children
    data = [{ "id": obj.pk , "username" : obj.user.username,"name" : obj.user.name, "email" : obj.user.email,"content": obj.content ,"retweet_count": obj.retweet.count() ,"likes_count":obj.likes.count() , "coverphoto":coverphoto(obj),"date_posted": obj.date_posted,"profilephoto":profilephoto(obj)  ,"replies_count" : obj.replies.count()} for obj in replies]
    return data

def coverphoto(obj):
    if obj.user.profile.coverphoto:
        return f"http://localhost:8000{obj.user.profile.coverphoto.url}"
    return f"http://localhost:8000{obj.user.profile.default.url}"

def profilephoto(obj):
    if obj.user.profile.profilephoto:
        return f"http://localhost:8000{obj.user.profile.profilephoto.url}"
    return f"http://localhost:8000{obj.user.profile.default.url}"

class NotTweetSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Tweets
        fields = [ "id", "content", "user" ]
        









  
        

