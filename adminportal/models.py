from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    # bio = models.TextField(null=True)
    code = models.UUIDField(null=True)
    codeCreated = models.DateTimeField(null=True)
    auth = models.BooleanField(null=True)
    adminAccess = models.BooleanField(null=True)
    # avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    