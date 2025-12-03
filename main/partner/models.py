from django.db import models

from django.core import validators

from django.core.exceptions import ValidationError

def passwordcheck(value):
   if len(str(value))<6:
      raise ValidationError("password is too short")



class PartnerSignup(models.Model):
    username=models.CharField(max_length=100,default="user")
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=100,validators=[passwordcheck])
    confirmpass=models.CharField(max_length=100)









# Create your models here.
class Restaurants(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    Location = models.CharField(max_length=150, null=True, blank=True)
    Timeopen=models.TimeField(blank=True,null=True)
    Closetime=models.TimeField(blank=True,null=True)
    image = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    Isopen=models.BooleanField(default=True)
    rating = models.FloatField(default=0, null=True, blank=True)
    deliverytime=models.FloatField(default=30)
    
    class Meta:
        verbose_name_plural = "Restaurants"
    def __str__(self):
      return self.Name


class Category(models.Model):
   restaurant=models.ForeignKey(Restaurants,on_delete=models.CASCADE,related_name="categories")
   name=models.CharField(max_length=30)

   def __str__(self):
      return f"{self.name}-{self.restaurant.Name}"
   

class Item(models.Model):
   VEG='veg'
   NON_VEG='nonveg'

   Foodchoice=[
      (VEG,'Veg'),
      (NON_VEG,'Non-veg')
   ]
   

   category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="item")   
   image=models.URLField(blank=True)
   name=models.CharField(max_length=100)
   description=models.CharField(max_length=300)
   rating=models.FloatField(max_length=20)
   price=models.FloatField(max_length=20)
   food_type=models.CharField(max_length=10,choices=Foodchoice)
   is_available=models.BooleanField(default=True)
   total_orders=models.IntegerField(default=0)


   def __str__(self):
      return self.name

