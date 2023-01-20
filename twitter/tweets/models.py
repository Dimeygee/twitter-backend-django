from django.db import models
from django.conf import settings

class TweetsManager(models.Manager):
    def all(self):
        query = super(TweetsManager, self).filter(parent=None)
        return query

class Tweets(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content=models.TextField(max_length=200)
    likes=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked')
    date_posted = models.DateTimeField(auto_now_add=True) 
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE, related_name='replies')
    retweet=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='retweet')
    image = models.ImageField(null=True, upload_to="tweetsimages")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-date_posted']
        verbose_name='Tweet'
        verbose_name_plural = 'Tweets'

    objects = TweetsManager()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    @property
    def get_children(self):
        return Tweets.objects.filter(parent=self)
    
    def get_comments(self):
        return Tweets.objects.filter(parent=self)

