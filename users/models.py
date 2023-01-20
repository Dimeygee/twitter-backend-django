from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,username,email,name,password=None):
        if username is None:
            raise ValueError('Users must have username')

        if email is None:
            raise ValueError('Users must have an email address.')

        if name is None:
            raise ValueError('Users must have a name.')

        user = self.model(email=self.normalize_email(email),username=username,name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,username,email,name,password=None):
        user = self.create_user(email=self.normalize_email(email),username=username,name=name,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user 


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True,max_length=50,unique=True)
    email = models.EmailField(db_index=True,unique=True) 
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','name']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.username}"

       
