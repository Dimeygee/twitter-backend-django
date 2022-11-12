from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions
from .serializers import  TweetSerialzer
from .models import Tweets 
from django.db.models import Q
from notifications.models import Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class getTweetView(APIView):
    
    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        queryset = Tweets.objects.all()
        serializer = self.serializer_class(queryset,many=True,context={ 'request': request })
        return Response(serializer.data,status=status.HTTP_200_OK)

    
class CreateTweetView(APIView): 

    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TweetDetailView(APIView):

    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)

    def get(self,request,pk=None):
        tweet = Tweets.objects.get(pk=pk)
        serializer = self.serializer_class(tweet, context={ 'request': request })
        return Response(serializer.data)

    def delete(self,request,pk=None):
        tweet = Tweets.objects.get(pk=pk)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReplyTweetView(APIView):

    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def get(self,request,pk=None):
        tweet = Tweets.objects.get(pk=pk)
        comments = tweet.get_comments() 
        serializer = self.serializer_class(comments,many=True, context={'request': request})
        return Response(serializer.data)

    def post(self,request,pk=None):
        parentTweet = Tweets.objects.get(pk=pk)
        print(parentTweet)
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(parent=parentTweet,user=request.user)
        if request.user != parentTweet.user:
            Notification.objects.get_or_create(notification_type="R",tweet=parentTweet,to_user=parentTweet.user,from_user=request.user)
        return Response(serializer.data)
    
class LikeOrUnlikeTweet(APIView):
    
    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)

    def get(self,request,pk=None):
        tweet = Tweets.objects.get(pk=pk)
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
            Notification.objects.get_or_create(notification_type="L",tweet=tweet,to_user=tweet.user,from_user=request.user)
        serializer = self.serializer_class(tweet, context={ 'request': request })
        return Response(serializer.data)


class RetweetView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerialzer
        
    def get(self, request, pk=None):
        tweet = Tweets.objects.get(pk=pk)
        if tweet.user == request.user:
            raise exceptions.APIException("Can't Retweet your Tweet")
        if request.user in tweet.retweet.all() :
            tweet.retweet.remove(request.user)
            serializer = self.serializer_class(tweet, context={ 'request': request })
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            tweet.retweet.add(request.user)
            serializer = self.serializer_class(tweet, context={ 'request': request })
            Notification.objects.get_or_create(notification_type="RT",tweet=tweet,to_user=tweet.user,from_user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TweetsListView(APIView):

    serializer_class = TweetSerialzer
    permission_classes = (IsAuthenticated,)

    def get(self, request,username, type=None):
        if str(type) == "tweet_only":
            retweet = Q()
            tweets = Tweets.objects.filter(user__username=username)
            for tweet in tweets:
                if username in tweet.retweet.all():
                    retweet.append(tweet)
            userTweets = retweet | tweets 
            serializer = self.serializer_class(userTweets, may=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if type == 'tweet&replies':
            tweets = Tweets.objects.filter(user__username=username)
            re_tweet = Tweets.objects.filter(retweet__user__username=username)
            userTweets = re_tweet | tweets
            serializer = self.serializer_class(userTweets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if type == 'liked':
            likes = Tweets.objects.filter(likes__user__username=username)
            likedTweets = likes
            serializer = self.serializer_class(likedTweets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class TweetsSearchView(APIView):

    serializer_class = TweetSerialzer

    def post(self, request):
        query = request.data['query']
        tweets = Tweets.objects.filter(content__icontains=query)
        serializer = TweetSerialzer(tweets,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


        
            
        







