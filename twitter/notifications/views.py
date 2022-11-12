from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from notifications.serializer import NotifcationSerializer
from notifications.models import Notification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class NotifcationListView(APIView):
    
    serializer_class = NotifcationSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request): 
        not_count = Notification.objects.filter(to_user=request.user).count()
        notifications = Notification.objects.filter(to_user=request.user)
        serializer= self.serializer_class(notifications, many=True)
        return Response({ "data": serializer.data, "not_count": not_count }, status=status.HTTP_200_OK)
        
        
class NotificationSeenView(APIView):
    
    def post(self, request, pk=None):
        notification = get_object_or_404(Notification,pk=pk)
        notification.seen = True
        notification.save()
        return Response({ "notification_seen" : True })
        
        
        
    
        
