from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from authentication.models import Cart
from partner.models import Restaurants,Item,Order,OrderItem
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
           
  
    if 'handle_cart' in request.POST:
        
        x = request.POST.get('handle_cart')

        itemid, cat_id, res_id, AD = x.split(',')

        itemid = int(itemid)
        cat_id = int(cat_id)
        res_id = int(res_id)
    
    
        print("cat_id=", cat_id)
        print("item_id=", itemid)
        print("res_id=", res_id)
        print("ADD=",AD)



        if not Cart.objects.filter(user=request.user, restaurantid=res_id).exists():
            Cart.objects.filter(user=request.user, restaurantid=res_id).delete()

       
        if Cart.objects.filter(user=request.user, item_id=itemid).exists():
            
            if AD=="ADD":
                cart = Cart.objects.get(item_id=itemid)
                cart.quantity+=1
                cart.save()
            else:
                cart = Cart.objects.get(item_id=itemid)
                cart.quantity-=1
                cart.save()
                if cart.quantity==0:
                    cart.delete()  
        
        else:
            
            restaurant=get_object_or_404(Restaurants,id=res_id)
            item_data = Item.objects.get(category__restaurant=restaurant,id=itemid)
            print("itemid:", itemid, type(itemid))
            
            print(item_data.price)
            Cart.objects.create(
                user=request.user,
                restaurantid=id,
                item_id=item_data.id,
                item=item_data.name,
                price=item_data.price,
                food_type=item_data.food_type,
                quantity=1
                )
    
        
   
    return render(request,'cart/cart.html',{'total':totalprice,'cart':cart,'restaurant':Restaurant})



def track(request):
    return render(request,'cart/track_order.html')
