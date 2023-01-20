from django.db import models
from django.conf import settings

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio=models.TextField(blank=True,max_length=100)
    follows=models.ManyToManyField('self',blank=True,related_name='follows_user',symmetrical=False)
    joined=models.DateField(auto_now=True)
    location = models.CharField(max_length=200,null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    profilephoto  = models.ImageField(default='profile.jpg',upload_to='profile')
    coverphoto  = models.ImageField(default='cover.jpg',upload_to='cover')  

    def __str__(self):
        return self.user.username

    def follow(self,profile):
        return self.follows.add(profile)

    def unfollow(self, profile):
        return self.follows.remove(profile)

    def is_following(self,profile):
        return self.follows.filter(pk=profile.pk).exists()

    def is_following_user(self,profile):
        return self.follows_user.filter(pk=profile.pk).exists()



