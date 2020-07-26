from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, blank=False)
    pan = models.CharField(max_length=11, blank=False)
    accountNo = models.CharField(max_length=20, blank=True)
    accountRefNo = models.CharField(max_length=20, blank=True)
    uuid = models.CharField(max_length=100, blank=True)
    txnid = models.CharField(max_length=100, blank=True)
    sid = models.CharField(max_length=100, blank=True)
    userID = models.CharField(max_length=100, blank=True)
    sessionid = models.CharField(max_length=1000, blank=True)
    rid = models.CharField(max_length=1000, blank=True)
    ftoken = models.TextField( blank=True)
    banklink = models.BooleanField(default=False)
    profile_complete = models.BooleanField(default=False)

class Settings(models.Model):
    google_auth_token = models.TextField(blank=True)