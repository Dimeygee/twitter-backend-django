from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from users.models import User
from django.shortcuts import redirect
from rest_framework import  status, serializers
from rest_framework.parsers import MultiPartParser, FormParser ,JSONParser, FileUploadParser
#from rest_framework.exceptions import NotFound
#from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UpdateUserProfile


class UserProfileView(APIView):

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        userprofile = Profile.objects.get(user__username=username)
        serializer = self.serializer_class(userprofile,context={'request': request})
        return Response(serializer.data)
    

class UpdateProfileSerializer(APIView):
    
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserProfile
    
    def put(self, request):
        userprofile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(userprofile,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            print(serializer.errors)
            return Response(serializer.errors)
    
class UserGetProfileView(APIView):
    
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        username = request.user.username
        userprofile = Profile.objects.get(user=username)
        serializer = self.serializer_class(userprofile,context={'request': request})
        return Response(serializer.data)
    

class ProfileFollowOrUnFollow(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    

    def delete(self,request,pk=None):
        follower = Profile.objects.get(user=request.user)
        followee = get_object_or_404(Profile, pk=pk)

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={'request' : request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, pk=None):
        follower = Profile.objects.get(user=request.user)
        followee = get_object_or_404(Profile, pk=pk)
        followee_user = get_object_or_404(User, pk=pk)
        
        print(follower)
        
        print(followee)

        if follower.pk is followee.pk:
            raise serializers.ValidationError("You can't follow yourself")

        follower.follow(followee)
        Notification.objects.get_or_create(notification_type="F",to_user=followee_user, from_user=request.user)
        serializer = self.serializer_class(followee, context={'request' : request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        















