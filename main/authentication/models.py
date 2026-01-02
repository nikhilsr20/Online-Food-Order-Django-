from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    restaurantid=models.IntegerField(null=True, blank=True)
    item_id=models.IntegerField()
    item=models.CharField(max_length=50)
    quantity=models.IntegerField(default=1)
    food_type=models.CharField(max_length=20)
    price=models.DecimalField( max_digits=10, decimal_places=2)
    


    def total_price(self):
         return self.quantity * self.price

    def __str__(self):
          return f"{self.item} ({self.user.username})"
