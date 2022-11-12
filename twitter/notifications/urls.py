from django.urls import path
from .views import NotifcationListView, NotificationSeenView

urlpatterns = [
    path("get_notifications/", NotifcationListView.as_view()),
    path("seen_notifications/<int:pk>", NotificationSeenView.as_view())
]