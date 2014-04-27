from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(models.Model):
    """
    Custom user class.
    """
    email = models.EmailField('email address', unique=True, db_index=True)
    password = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    laboratory = models.CharField(max_length=20)
    telnumber = models.CharField(max_length=20)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

   

    def __unicode__(self):
        return self.email 