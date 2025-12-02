from django.shortcuts import render
from django.shortcuts import redirect
from .forms import PartnerSignupForm,PartnerLoginForm
from .models import PartnerSignup
# Create your views here.
def signup(request):
    if request.method=='POST':
        form=PartnerSignupForm(request.POST)
        print(request.POST)
        

        if form.is_valid():
            phone=form.cleaned_data.get('phone')
            if PartnerSignup.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Phone number is already registered')
            else:
                request.session['users-phone']=phone
                form.save()
                return redirect('partner-main')
            
    else:
        form = PartnerSignupForm()        
            
    return render(request,'partner/partner.html',{'form':form})


def main(request):
    return render (request,'partner/partner-main.html')


def login(request):
    if request.method=='POST':
        form=PartnerLoginForm(request.POST)
        print(request.POST)
        
        
        if form.is_valid():
            phone=form.cleaned_data.get('phone')
            request.session['users-phone']=phone
            return redirect('partner-main')
    else:
        form = PartnerLoginForm()        
            
    return render(request,'partner/partnerlogin.html',{'form':form})
