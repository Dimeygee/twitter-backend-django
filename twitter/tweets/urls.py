from django.urls import path
from .views import getTweetView, TweetDetailView, ReplyTweetView, CreateTweetView,RetweetView, TweetsListView,LikeOrUnlikeTweet

urlpatterns = [
    path('tweets/',getTweetView.as_view()),
    path('tweet/<int:pk>/',TweetDetailView.as_view()),
    path('replytweet/<int:pk>/',ReplyTweetView.as_view()),
    path('retweet/<int:pk>/',RetweetView.as_view()),
    path('createtweet/',CreateTweetView.as_view()),
    path('tweetlist/<str:username>/<str:type>',TweetsListView.as_view()),
    path('likeorunlike/<int:pk>',LikeOrUnlikeTweet.as_view()),
]
