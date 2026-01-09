from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from authentication.models import Cart
from partner.models import Restaurants,Item,Order,OrderItem
from django.template.loader import render_to_string
# Create your views here.
def cart(request):
    if not request.user.is_authenticated:
        return redirect('register')
    
    totalprice=0
    Restaurant=None
    cart=Cart.objects.filter(user=request.user)
    if cart.exists():
        resid=cart[0].restaurantid
        print(resid)
        Restaurant=get_object_or_404(Restaurants,id=resid)
        
        for i in cart:
            totalprice+=(i.quantity*i.price)

    
    if 'confirm_order' in request.POST:
        if Cart.objects.filter(user=request.user).exists():
            cart_data=Cart.objects.filter(user=request.user)
            res_id=cart_data[0].restaurantid
            order=Order.objects.create(
               restaurant_id=res_id,
               customer_name=request.user.username,
               customer_phone=request.session.get('phone'),
               customer_address="none",
               order_amount=totalprice,
            )
            for item in cart_data:
             OrderItem.objects.create(
                order=order,
                order_item_name=item.item,
                order_item_quantity=item.quantity,
            )
            cart_data.delete() 
            return redirect('trackorder')
        
   
    return render(request,'cart/cart.html',{'total':totalprice,'cart':cart,'restaurant':Restaurant})



def track(request):
    return render(request,'cart/track_order.html')


def update_my_cart(request):
        print("🔥 update_my_cart hit")
        itemid = int(request.POST.get("item-id"))
        AD=request.POST.get("action")

        if AD=="ADD":
            cart = Cart.objects.get(item_id=itemid)
            cart.quantity+=1
            cart.save()
        else:
            cart = Cart.objects.get(item_id=itemid)
            cart.quantity-=1
            if cart.quantity==0:
                cart.delete()  
                return HttpResponse("")
            cart.save()

        cart = Cart.objects.filter(user=request.user, item_id=itemid).first()
        user_cart = Cart.objects.filter(user=request.user)
        total = sum(i.quantity * i.price for i in user_cart)

        html = ""

        if cart:
            html += render_to_string("cart/cartpartial.html",{"i": cart}, request)

    # 🔥 ALWAYS send total update
        html += render_to_string("cart/cart_total_oob.html",{"total": total},request)

        return HttpResponse(html)
        


