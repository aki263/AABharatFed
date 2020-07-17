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
    banklink = models.BooleanField(default=False)
