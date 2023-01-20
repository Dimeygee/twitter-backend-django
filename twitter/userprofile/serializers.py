from wsgiref import validate
from django.db.models import fields
from rest_framework import serializers
from userprofile.models import Profile
from rest_framework.renderers import JSONRenderer
from users.models import User

def getProfilePhoto(obj):
    if obj.profilephoto:
        return f"http://localhost:8000{obj.profilephoto.url}" 
    return f"http://localhost:8000{obj.profilephoto.default}" 

def getCoverPhoto(obj):
    if obj.coverphoto:
        return f"http://localhost:8000{obj.coverphoto.url}" 
    return f"http://localhost:8000{obj.coverphoto.default}" 


def getFollows(obj):
    follows = obj.follows.all()
    data = [{ "id": obj.pk, "username": obj.user.username,"bio": obj.bio ,"name" : obj.user.name,"followers_count": obj.follows.count(), "following_count" : obj.follows_user.count(), "profilephoto": getProfilePhoto(obj),  "coverphoto": getCoverPhoto(obj)} for obj in follows ]
    return data

def getFollowers(obj):
    followers = obj.follows_user.all()
    data = [{ "id": obj.pk, "username": obj.user.username,"name" : obj.user.name,"bio": obj.bio ,"followers_count": obj.follows.count(), "following_count" : obj.follows_user.count(),"profilephoto": getProfilePhoto(obj),  "coverphoto": getCoverPhoto(obj)} for obj in followers]
    return data


class ProfileSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    name = serializers.CharField(source='user.name',read_only=True)
    follows =serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profilephoto = serializers.SerializerMethodField()
    coverphoto = serializers.SerializerMethodField()
    isfollowing = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id','username','name',"link","joined",'bio','location','follows','profilephoto','coverphoto','followers_count', 'following_count', 'followers', 'isfollowing']
        read_only_fields = ('username',) 
    
    def get_followers(self, obj):
       return getFollowers(obj)

    def get_follows(self, obj):
        return getFollows(obj)
    
    def get_profilephoto(self, instance):
        return getProfilePhoto(instance)

    def get_coverphoto(self, instance):
        return getCoverPhoto(instance)

    def get_followers_count(self, instance):
        return instance.follows_user.count()

    def get_following_count(self, instance):
        return instance.follows.count()

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance

    def get_isfollowing(self, instance):
        profile = self.context.get("request").user.profile
        return instance.is_following_user(profile)
        


        
        
class UserInfoChat(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    name= serializers.CharField(source='user.name',read_only=True)
    profilephoto = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ["id", "username","name","profilephoto"]
        
    def get_profilephoto(self, obj):
        if obj.profilephoto:
            return f"http://localhost:8000{obj.profilephoto.url}" 
        return f"http://localhost:8000{obj.profilephoto.default}" 
    
class UpdateUserProfile(serializers.ModelSerializer):
    
    name = serializers.CharField(source="user.name")
    
    class Meta: 
        model = Profile
        fields = ["name","bio","location","link","profilephoto","coverphoto"]
        
    def update(self, instance, validated_data):
        profile_name = validated_data.get("user", {})
        
        profile = instance.user
        
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.link = validated_data.get('link', instance.link)
        instance.profilephoto = validated_data.get('profilephoto', instance.profilephoto)
        instance.coverphoto = validated_data.get('coverphoto', instance.coverphoto)
        
        instance.save()
        
        
        profile.name = profile_name.get("name",  profile.name)
        
        profile.save()
        
        return instance
    

class LessUserProfile(serializers.ModelSerializer):
    
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profilephoto = serializers.SerializerMethodField()
    coverphoto = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ["followers_count","following_count", "profilephoto", "coverphoto"]
        
    def get_profilephoto(self, instance):
        return getProfilePhoto(instance)

    def get_coverphoto(self, instance):
        return getCoverPhoto(instance)

    def get_followers_count(self, instance):
        return instance.follows_user.count()

    def get_following_count(self, instance):
        return instance.follows.count()
        
        

    

        

    