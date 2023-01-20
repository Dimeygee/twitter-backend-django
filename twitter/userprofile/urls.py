from django.urls import path
from .views import  UserProfileView, ProfileFollowOrUnFollow, UpdateProfileSerializer


urlpatterns = [
    path('api/auth/<str:username>', UserProfileView.as_view()),
    path('editprofile/', UpdateProfileSerializer.as_view()),
    path('followorufollow/<int:pk>',ProfileFollowOrUnFollow.as_view()),
]