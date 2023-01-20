from rest_framework.response import Response 
from rest_framework.views import APIView
from .models import HashTag
from .serializers import TrendingTweetsSerialzers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tweets.models import Tweets
from tweets.serializers import TweetSerialzer

class HasTagView(APIView):

    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)

    def get(self,request,hash):
        tweets = Tweets.objects.filter(content__contains=hash)
        serializer = self.serializer_class(tweets, many=True, context={ 'request': request })
        return Response(serializer.data,status=status.HTTP_200_OK)

class TrendsView(APIView):

    serializer_class = TrendingTweetsSerialzers
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        Trends = HashTag.objects.all()[:8]
        serializer = self.serializer_class(Trends, many=True, context={ 'request': request })
        return Response(serializer.data, status=status.HTTP_200_OK)

