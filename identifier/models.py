from email.policy import default
from enum import unique
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from contenu.models import video

#models for the user

#we'll use the BaseUsermanager solution to allow customizability in case we need it

#for the first class we need to define the main methods of the user class with the attributes that would be required
class utilisateur_model(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
#for this class we'll make the objects attribute inheret the attribute of the top class then we will explicitly declare the class fields
class utilisateur(AbstractBaseUser):
    username = models.CharField(max_length=100 ,unique=True)
    USERNAME_FIELD = 'username'
    anime_prefere = models.ManyToManyField(video, default=None)
    is_admin = models.BooleanField(default=False)
    is_friend = models.BooleanField(default=False)
   
    objects = utilisateur_model()

    #we need to declaree some methods in order to allow the creation of a superuser 
    def has_perm(self, perm, obj=None):
        if self.is_admin == True :
            return True
        else:
            return False


    def has_module_perms(self, app_label):
        if self.is_admin == True :
            return True
        else:
            return False
        

    def is_staff(self):
        return self.is_admin
