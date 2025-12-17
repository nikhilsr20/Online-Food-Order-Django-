from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .forms import PartnerSignupForm,PartnerLoginForm,RestaurantsForm
from .models import PartnerSignup,Restaurants
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
    # if request.method=="POST":
    #     res_data=get_object_or_404()

    return render(request,'partner/partner-menu.html')



def orders(request):
    return render(request,"partner/partner-orders.html")


