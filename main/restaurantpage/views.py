from django.shortcuts import render,get_object_or_404
from partner.models import Restaurants,Item
from authentication.models import Cart



   
# Create your views here.

def restaurant(request,id):
 
    
  


    if 'add_to_cart' in request.POST:
        x = request.POST.get('add_to_cart')

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

         



    restaurant=get_object_or_404(Restaurants,id=id)
    print(restaurant)

    category=restaurant.categories.all()

    items=Item.objects.filter(category__restaurant=restaurant)

    q=[]
    for i in items:
        x = Cart.objects.filter(item_id=i.id).first()
        if x:
            q.append({
            "id":i.id,    
            "quantity":x.quantity,
            })
        else:
            q.append({
            "id":i.id,    
            "quantity": 0,
            })   


    return render(request,'restaurantpage/res.html',{'category':category,'items':items,'restaurant':restaurant,'q':q})







