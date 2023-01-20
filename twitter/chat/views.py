from django.http.response import HttpResponse
from rest_framework import permissions
from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer
from .serializer import ChatUserListSerializer, ChatSerializer, MessageSerializer
from rest_framework.views import APIView 
from django.shortcuts import get_object_or_404
from .models import Message, Chat
from rest_framework.response import Response
from users.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from userprofile.serializers import UserInfoChat


class ChatUsersListView(APIView):
   
    serializer_class = ChatUserListSerializer
    
    def get(self,request):
        messages = Message.objects.filter(user=request.user)
        users = []
        for message in messages:
            if message.chatroom.user1 == request.user:
                users.append(message.chatroom.user2)
            elif message.chatroom.user2 == request.user:
                users.append(message.chatroom.user1)
                
        serializer = self.serializer_class(users,many=True)
        return Response(serializer.data)
    
    
class ChatMessagesView(APIView):
    
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,username):
        u2 = get_object_or_404(User, username=username)
        u1 = request.user
        room = Chat.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2,user2=u1)).first()
        messages = Message.objects.by_room(room)
        serializer = self.serializer_class(messages,many=True)
        return Response(serializer.data)
    
    
class SearchUser(APIView):
    
    serializer_class = UserInfoChat
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        search = request.query_params.get("search", "")
        myprofile = Profile.objects.get(user=request.user)
        user = myprofile.follows.filter(Q(user__username__icontains=search) | Q(user__name__icontains=search))
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)
        
        
        



