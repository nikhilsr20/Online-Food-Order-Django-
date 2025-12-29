from django.shortcuts import render,get_object_or_404
from partner.models import Restaurants,Item
# Create your views here.

def restaurant(request,id):
    # restaurant=Restaurants.objects.get(id=id)

    restaurant=get_object_or_404(Restaurants,id=id)
    print(restaurant)

    category=restaurant.categories.all()

    items=Item.objects.filter(category__restaurant=restaurant)

    return render(request,'restaurantpage/res.html',{'category':category,'items':items,'restaurant':restaurant})

