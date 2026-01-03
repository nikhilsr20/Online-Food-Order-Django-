from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from authentication.models import Cart
from partner.models import Restaurants
# Create your views here.
def cart(request):
    totalprice=0
    Restaurant=None
    cart=Cart.objects.filter(user=request.user)
    if cart.exists():
        resid=cart[0].restaurantid
        print(resid)
        Restaurant=get_object_or_404(Restaurants,id=resid)
        
        for i in cart:
            totalprice+=(i.quantity*i.price)

        
   
    return render(request,'cart/cart.html',{'total':totalprice,'cart':cart,'restaurant':Restaurant})