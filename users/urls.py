from django.urls import path, include
from .views import ResetPasswordVIew, UserDetailView, MyUserView

urlpatterns = [
  path('api/auth/resetpassword', ResetPasswordVIew.as_view()),
  #path('api/auth/user/<str:username>', UserDetailView.as_view()),
  path('me', MyUserView.as_view()),
]