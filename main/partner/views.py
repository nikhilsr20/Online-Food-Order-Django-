from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .forms import PartnerSignupForm,PartnerLoginForm,RestaurantsForm,CategoryForm,ItemForm,EditItemForm
from .models import PartnerSignup,Restaurants,Category,Item,Order,OrderItem
from django.views.decorators.cache import never_cache
from datetime import date, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Sum

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = PartnerSignupForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            if PartnerSignup.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Phone number is already registered')
            else:
                user = form.save()   

                request.session['username'] = user.username
                request.session['users-phone'] = phone

                return redirect('partner-main')

    else:
        form = PartnerSignupForm()

    return render(request, 'partner/partner.html', {'form': form})  
            
    return render(request,'partner/partner.html',{'form':form})


def main(request):
    today = timezone.now().date()
    x = Order.objects.filter(order_date=today)
    t = timezone.now().date().isoformat() 
    selected_date = request.COOKIES.get('selected_date')
    if selected_date:
        selected_date = date.fromisoformat(selected_date)  # string → date
    else:
        selected_date = timezone.now().date()

    if request.GET.get('change')=='back':
        
        selected_date = selected_date - timedelta(days=1)  
        x = Order.objects.filter(order_date=selected_date)
        t=selected_date.isoformat()
    elif request.GET.get('change')=='next' and selected_date < today :
        
        selected_date = selected_date + timedelta(days=1)  
        x = Order.objects.filter(order_date=selected_date)
        t=selected_date.isoformat()    
    
  
    
    response= HttpResponse("Date cookie set ✅")
    
    
    display_date = selected_date.strftime("%d %b")
    
    if selected_date==timezone.now().date():
        display_date="Today"
    



    
    date_orders=x.count()
    date_revenue = x.aggregate(total_revenue=Sum('order_amount'))['total_revenue'] or 0
    date_pending=x.filter(status='pending').count()
    response = render(
        request,
        'partner/partner-main.html',
        {
            'date_orders': date_orders,
            'date_revenue': date_revenue,
            'date_pending': date_pending,
            'displaydate': display_date,
        }
    )

    
    response.set_cookie(
        'selected_date',
        selected_date.isoformat(),
        max_age=60*60*24
    )

    return response

    


def login(request):
    request.session.flush()
    if request.method=='POST':
        form=PartnerLoginForm(request.POST)
        print(request.POST)
        
        
        if form.is_valid():
            phone=form.cleaned_data.get('phone')
            name=PartnerSignup.objects.get(phone=phone)
            name=name.username
            request.session['username']=name
            request.session['users-phone']=phone
            return redirect('partner-main')
    else:
        form = PartnerLoginForm()        
            
    return render(request,'partner/partnerlogin.html',{'form':form})


def logout(request):
    request.session.flush()
    return redirect('partnerlogin')


def profile(request):
    phone = request.session.get('users-phone')
    user_instance=get_object_or_404(PartnerSignup,phone=phone)
    
    print(user_instance)

    try:
        restaurant_instance=user_instance.USER
        print(restaurant_instance)
    except Restaurants.DoesNotExist:
        restaurant_instance=None


  
    if request.method=='POST':
        form=RestaurantsForm(request.POST,request.FILES,instance=restaurant_instance)
        print(form)
        if form.is_valid():
            print("saving form")
            res=form.save(commit=False)
            res.user=user_instance
            res.save()
    else:
        form=RestaurantsForm(instance=restaurant_instance)
    return render(request,'partner/partner-profile.html',{'form':form})




# may include bugs so abhi shi krna h  menu wala 


def menu(request):
    phone = request.session.get('users-phone')
    
    user=get_object_or_404(PartnerSignup,phone=phone)
    
    

    try:
        restaurant = user.USER
       
    except Restaurants.DoesNotExist:
   
        return redirect('partner-profile')
    
    



    categories = restaurant.categories.all()
    
    category_id=request.POST.get('category_id')

    

    category = Category.objects.filter(
                    id=category_id,
                    restaurant=restaurant
                ).first()
    
    print(category)
    
    items_list = Item.objects.filter(category__restaurant=restaurant)

    # <button type="submit" name="edit_item" value="{{ item.id }}"> aesa button bnana h abhi 
    
   
        
    

    if 'add_item' in request.POST:
        print("patakha")
        item_instance=None
    elif 'edit_item' in request.POST:
        value = request.POST.get('edit_item')
        v=int(value)
        item_instance=Item.objects.filter(id=v,category=category).first()    


    


    
    if request.method=="POST":
        
        if 'add_category' in request.POST:
           
            item_form=ItemForm()
            edit_form=EditItemForm()
            form = CategoryForm(request.POST)
           
            if form.is_valid():
                print("hello")
                cat = form.save(commit=False)
                cat.restaurant = restaurant
                cat.save()
                
        elif 'add_item' in request.POST:
            print("hello")
            item_form=ItemForm(request.POST, request.FILES,instance=item_instance) 
            form=CategoryForm()
            edit_form=EditItemForm()
            print("hello")
            print(item_form)
            if item_form.is_valid():
                print("heello")
                item = item_form.save(commit=False)
              
                item.category=category
                item.save()

        elif 'edit_item' in request.POST:
            
            edit_form=EditItemForm(request.POST, request.FILES,instance=item_instance) 
            form=CategoryForm()
            item_form=ItemForm()
            
            
            if edit_form.is_valid():
                
                edit = edit_form.save(commit=False)
              
                edit.category=category
                edit.save()        

    else:
        form=CategoryForm()
        edit_form=EditItemForm()
        item_form=ItemForm()

    # categories=Restaurant.categories.all()

        
    return render(request,'partner/partner-menu.html',{'form':form,'categories':categories,'item_form': item_form,'edit_form':edit_form,'item_list':items_list})
   


def orders(request):
    phone = request.session.get('users-phone')
    user_instance = get_object_or_404(PartnerSignup, phone=phone)

    restaurant = Restaurants.objects.filter(user=user_instance).first()

    if request.method == "POST":
        if 'complete_action' in request.POST:
            val = int(request.POST.get('complete_action'))
            x = Order.objects.get(id=val)
            x.status = 'completed'
            x.save()

        if 'cancel_action' in request.POST:
            val = int(request.POST.get('cancel_action'))
            x = Order.objects.get(id=val)
            x.status = 'cancelled'
            x.save()

    orders = Order.objects.filter(restaurant=restaurant).prefetch_related('items')

    return render(request, "partner/partner-orders.html", {
        'orders': orders,
        'restaurant': restaurant
    })