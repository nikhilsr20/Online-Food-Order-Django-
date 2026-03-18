from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from authentication.models import Cart  
from .forms import Addressform
from partner.models import Restaurants,Item,Order,OrderItem
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import CurrAddress
from .models import DeliveryAddress

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.
def cart(request):
    addresses=DeliveryAddress.objects.all()
    form = Addressform()
    if request.method == 'POST' and 'newaddress' in request.POST:
        
        form = Addressform(request.POST)
        print(form)
        if form.is_valid():
            print("hello")

            x=form.save(commit=False)
            x.userr=request.user
            x.save()
            return redirect('cart')
    



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
            print("🔥 SENDING WS EVENT")
            channel_layer=get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                
                 f"orders_{res_id}",
                 {
                    "type": "new_order",
                    "order_id": order.id,
                }
                )
            
            for item in cart_data:
             OrderItem.objects.create(
                order=order,
                order_item_name=item.item,
                order_item_quantity=item.quantity,
            )
            cart_data.delete() 
            return redirect('trackorder')
        
    current = CurrAddress.objects.filter(user_id=request.user.id).first()
    curr_address = ""
    if current:
        curr_address = current.curraddress
    return render(request,'cart/cart.html',{'total':totalprice,'cart':cart,'restaurant':Restaurant,'form':form,'addresses':addresses,'curr':curr_address})

def achange(request):
    if request.GET.get('address_id') is not None:
        y=request.GET.get('address_id') 
        print("ID:", y)
        add = get_object_or_404(
        DeliveryAddress,
        userr=request.user,
        id=y
        )
        print(add)
        address=""
        if add:
          address = f"{add.Flat}, {add.Address}, {add.Landmark}"

        x=CurrAddress.objects.filter(user_id=request.user)
        if not x:
            CurrAddress.objects.create(
                user_id=request.user.id,
                curraddress=address
            )
        else:
            x.update(curraddress=address)   
        return redirect('cart')
    
    elif request.GET.get('add_id') is not None:
        y=request.GET.get('add_id') 
        print("ID:", y)
        add = get_object_or_404(
        DeliveryAddress,
        userr=request.user,
        id=y
        )
        print(add)
        address=""
        if add:
          address = f"{add.Flat}, {add.Address}, {add.Landmark}"

        x=CurrAddress.objects.filter(user_id=request.user)
        if not x:
            CurrAddress.objects.create(
                user_id=request.user.id,
                curraddress=address
            )
        else:
            x.update(curraddress=address)   
        return redirect('home')


def track(request):
    return render(request,'cart/track_order.html')


def update_my_cart(request):
        print("🔥 update_my_cart hit")
        itemid = request.POST.get("item-id")
        AD=request.POST.get("action")
        if not itemid:
            return HttpResponse("")

        itemid = int(itemid)
        response = HttpResponse("")
        if AD=="ADD":
            cart = Cart.objects.get(item_id=itemid)
            cart.quantity+=1
            cart.save()
        else:
            cart = Cart.objects.get(item_id=itemid)
            cart.quantity-=1
            if cart.quantity==0:
                cart.delete() 
                if not Cart.objects.filter(user=request.user).exists():
                    # response = HttpResponse("")
                    response["HX-Redirect"] = reverse('cart')
                    return response 
                return HttpResponse("")
            
            cart.save()
        response["HX-Trigger"] = "cart-updated"
        
        cart = Cart.objects.filter(user=request.user, item_id=itemid).first()
        user_cart = Cart.objects.filter(user=request.user)
        total = sum(i.quantity * i.price for i in user_cart)

        html = ""

        if cart:
            html += render_to_string("cart/cartpartial.html",{"i": cart}, request)

    # 🔥 ALWAYS send total update
        html += render_to_string("cart/cart_total_oob.html",{"total": total},request)
        response.content=html
        print(response)
        return response






