from django.shortcuts import render
from partner.models import Restaurants

# Create your views here.
def home(request):

    Restaurant=Restaurants.objects.all()
    print(Restaurants)
    if request.user.is_authenticated:
        print("✅ User is logged in:", request.user)
    else:
        print("❌ User is not logged in")

    return render(request,"homepage/mainpage.html",{'Restaurant':Restaurant})


