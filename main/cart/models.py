from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DeliveryAddress(models.Model):
    userr=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userr")
    head=models.CharField(max_length=100)
    Address=models.CharField(max_length=300)
    Flat=models.CharField(max_length=100)
    Landmark=models.CharField(max_length=100)

    

