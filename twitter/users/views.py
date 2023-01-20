from rest_framework import HTTP_HEADER_ENCODING, authentication
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer
from .serializers import RegisterSerializer,LoginSerializer,ResetPasswordSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import User
from rest_framework.permissions import  IsAuthenticated
from django.db.models import Q
from userprofile.models import Profile




class UserDetailView(APIView):

    serializer_class = UserSerializer

    def get(self,request,username):
        user=User.objects.get(username=username)
        serializer=self.serializer_class(user)
        return Response(serializer.data)

    def put(self,request,username):
        user=get_object_or_404(User,username=username)
        serializer=self.serializer_class(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


class MyUserView(APIView):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        user=User.objects.get(username=request.user.username)
        serializer=self.serializer_class(user, context={ "request": request } )
        return Response(serializer.data)

class ResetPasswordVIew(APIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        oldpassword = serializer.validated_data['oldpassword']
        newpassword = serializer.validated_data['newpassword']
        if not user.check_password(oldpassword):
            return Response({'oldpassword': ['Wrong password']}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(newpassword)
        user.save()
        response = {
            'status': 'success',
            'code':status.HTTP_200_OK,
            'message':'Password updated successfully'
        }
        return Response(response)
    
class UserSearchView(APIView):
    
    serializer_class = ProfileSerializer
    
    def post(self, request):
        profile  =  Profile.objects.get(user__username=request.user.username)
        user = profile.follows.filter(Q(user__username=request.data) | Q(user__name=request.data))
        serializer = self.serializer_class(user)
        return Response(serializer.data)
        
        

        
