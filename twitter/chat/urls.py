from django.urls import path
from .views import ChatMessagesView, ChatUsersListView,SearchUser

urlpatterns = [
    path('users_chat_list/',ChatUsersListView.as_view()),
    path('search_user/',SearchUser.as_view()),
    path('user_chat_message/<str:username>',ChatMessagesView.as_view()),
]