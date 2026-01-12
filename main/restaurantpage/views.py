from django.shortcuts import render,get_object_or_404
from partner.models import Restaurants,Item
from authentication.models import Cart
from django.http import HttpResponse
from types import SimpleNamespace
from django.template.loader import render_to_string


   
# Create your views here.

def restaurant(request,id):
    restaurant=get_object_or_404(Restaurants,id=id)
    print(restaurant)

    category=restaurant.categories.all()

    items=Item.objects.filter(category__restaurant=restaurant)
    cart_map = {
        c.item_id: c.quantity
        for c in Cart.objects.filter(user=request.user, restaurantid=id)
    }

    # Temporary joined table
    temp_items = []

    for item in items:
        temp_items.append(
            SimpleNamespace(
                id=item.id,
                category_id=item.category_id,
                name=item.name,
                price=item.price,
                desciption=item.description,
                rating=item.rating,
                image=item.image,
                food_type=item.food_type,
                quantity=cart_map.get(item.id, 0)  # 👈 KEY LINE
            )
        )

  


    return render(request,'restaurantpage/res.html',{'category':category,'items':temp_items,'restaurant':restaurant})





def update_cart(request):
    itemid = int(request.POST.get("item_id"))
    res_id = request.POST.get("res_id")
    action = request.POST.get("action")

    # allow cart only from one restaurant
    Cart.objects.filter(user=request.user).exclude(restaurantid=res_id).delete()

    cart = Cart.objects.filter(
        user=request.user,
        restaurantid=res_id,
        item_id=itemid
    ).first()

    if cart:
        if action == "ADD":
            cart.quantity += 1
            cart.save()
        else:  # MINUS
            cart.quantity -= 1
            if cart.quantity == 0:
                cart.delete()
                cart = None
            else:
                cart.save()
    else:
        restaurant = get_object_or_404(Restaurants, id=res_id)
        item = get_object_or_404(Item, id=itemid)

        cart = Cart.objects.create(
            user=request.user,
            restaurantid=res_id,
            item_id=item.id,
            item=item.name,
            price=item.price,
            food_type=item.food_type,
            quantity=1
        )
    total=Cart.objects.filter(user=request.user).count()
    quantity = cart.quantity if cart else 0

    j = SimpleNamespace(
        id=itemid,
        quantity=quantity
    )

    restaurant = get_object_or_404(Restaurants, id=res_id)

    html=render_to_string(
        
        "restaurantpage/res_cart_update.html",
        {
            "j": j,
            "restaurant": restaurant,
           
        },request
    )

    html+=render_to_string(
        
        "restaurantpage/cart_count.html",
        {
           'cartlength':total
           
        }
        ,request
    )

    return HttpResponse(html)