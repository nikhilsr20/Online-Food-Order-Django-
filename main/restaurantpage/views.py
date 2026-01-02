from django.shortcuts import render,get_object_or_404
from partner.models import Restaurants,Item
from authentication.models import Cart
# Create your views here.

def restaurant(request,id):


    if 'add_to_cart' in request.POST:
        x = request.POST.get('add_to_cart')

        cat_id, itemid, res_id, AD = x.split(',')

        cat_id = int(cat_id)
        itemid = int(itemid)
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

                if cart.quantity==0:
                    cart.delete()  
        
        else:
            print("xxx")
            item_data = get_object_or_404(Item, id=itemid)
           
            print(item_data)
            Cart.objects.create(
                user=request.user,
                restaurantid=id,
                item_id=item_data.id,
                item=item_data.name,
                price=item_data.price,
                food_type=item_data.food_type,
                quantity=1
                )

         



    restaurant=get_object_or_404(Restaurants,id=id)
    print(restaurant)

    category=restaurant.categories.all()

    items=Item.objects.filter(category__restaurant=restaurant)

    return render(request,'restaurantpage/res.html',{'category':category,'items':items,'restaurant':restaurant})







