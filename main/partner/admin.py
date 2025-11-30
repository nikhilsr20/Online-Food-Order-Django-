from django.contrib import admin
from .models import Restaurants,Category,Item
# Register your models here.
admin.site.register(Restaurants)
admin.site.register(Category)
admin.site.register(Item)