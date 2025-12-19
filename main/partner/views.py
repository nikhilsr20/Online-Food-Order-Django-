from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .forms import PartnerSignupForm,PartnerLoginForm,RestaurantsForm,CategoryForm,ItemForm
from .models import PartnerSignup,Restaurants,Category,Item
from django.views.decorators.cache import never_cache

# Create your views here.
def signup(request):
    if request.method=='POST':
        form=PartnerSignupForm(request.POST)
        print(request.POST)
        

        if form.is_valid():
            phone=form.cleaned_data.get('phone')
            name=PartnerSignup.objects.filter(phone=phone)
            name=name.username
            
            if PartnerSignup.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Phone number is already registered')
            else:
                request.session['username']=name
                request.session['users-phone']=phone
                form.save()
                return redirect('partner-main')
            
    else:
        form = PartnerSignupForm()        
            
    return render(request,'partner/partner.html',{'form':form})


def main(request):
    return render (request,'partner/partner-main.html')


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

    try:
        restaurant_instance=user_instance.USER
    except Restaurants.DoesNotExist:
        restaurant_instance=None


  
    if request.method=='POST':
        form=RestaurantsForm(request.POST,request.FILES,instance=restaurant_instance)

        if form.is_valid():
          
            res=form.save(commit=False)
            res.user=user_instance
            res.save()

    else:
        form=RestaurantsForm(instance=restaurant_instance)
    return render(request,'partner/partner-profile.html',{'form':form})

def menu(request):
    phone = request.session.get('users-phone')
    user=get_object_or_404(PartnerSignup,phone=phone)

    try:
        Restaurant = user.USER
    except Restaurants.DoesNotExist:
        return redirect('partner-profile')
    
    categories = Restaurant.categories.all()
    
    
    category_id=request.POST.get('category_id')
    category = Category.objects.filter(
                    id=category_id,
                    restaurant=Restaurant
                ).first()

    
    items_list=category.items.all()

    # <button type="submit" name="edit_item" value="{{ item.id }}"> aesa button bnana h abhi 

    value = request.POST.get('edit_item')

    if 'add-item' in request.POST:
        item_instance=None
    else:
        item_instance=Item.objects.get(id=value,category=category).first()    


    


    
    if request.method=="POST":

        if 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                cat = category_form.save(commit=False)
                cat.restaurant = Restaurant
                cat.save()
                
        if 'add_item' in request.POST:
            item_form=ItemForm(request.POST, request.FILES,item_instance) 
            if item_form.is_valid():
                item = item_form.save(commit=False)
                # abhi put krni h 
                item.category=category
                item.save()

    else:
        form=CategoryForm()
        form=ItemForm()

    categories=Restaurant.categories.all()

        
    return render(request,'partner/partner-menu.html',{'form':form,'categories':categories,'item_form': item_form,})



def orders(request):
    return render(request,"partner/partner-orders.html")


