from .views import HasTagView, TrendsView
from django.urls import path


urlpatterns = [
    path("hashtag/<str:hash>",HasTagView.as_view()),
    path("trends",TrendsView.as_view()),
]