from django.db import models
from tweets.models import Tweets
from users.models import User


class Notification(models.Model):
    
    types = [
        ("L", "love"),
        ("R", "Reply"),
        ("M", "Message"),
        ("F", "follow"),
        ("RT", "retweet"),
    ]
    
    notification_type = models.CharField(max_length=2,choices=types,default=None)
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE,blank=True, null=True, related_name="+")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_to",null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_from",null=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return f"from {self.from_user} to {self.to_user}"
    
    
    
    
    
