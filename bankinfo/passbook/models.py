from django.db import models
from django import forms
from django.contrib.auth.models import User
# Create your models here.

class passbookInfoModel(models.Model):
    entry_created_date = models.DateField(auto_created=True,auto_now_add=True)
    particular = models.CharField(max_length=100)
    debit  = models.DecimalField(max_digits=14,decimal_places=2,default=0,blank=True)
    credit = models.DecimalField(max_digits=14,decimal_places=2,default=0,blank=True)
    balance = models.DecimalField(blank=True,default=0,max_digits=20,decimal_places=2)