from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from userprofile.serializers import LessUserProfile


class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username','name','email', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'], validated_data['email'],validated_data['name'], validated_data['password'])

    return user


class LoginSerializer(serializers.Serializer):

    email=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect credentials')

class UserSerializer(serializers.ModelSerializer):

    profile = LessUserProfile() 

    class Meta: 
        model=User
        fields=['id','name',"username","profile"]
  
        
  

class ResetPasswordSerializer(serializers.Serializer):

    oldpassword = serializers.CharField(write_only=True,required=True)
    newpassword = serializers.CharField(write_only=True, required=True)
    
    

    
