from django.db import models
from tweets.models import Tweets 

class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tweet = models.ManyToManyField(Tweets)

    def __str__(self):
        return self.name


