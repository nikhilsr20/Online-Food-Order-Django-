from django.shortcuts import render
from partner.models import Restaurants

from django.core.paginator import Paginator

# Create your views here.
def home(request):

    Restaurant=Restaurants.objects.all()

    paginator=Paginator(Restaurant,12)

    page_number=request.GET.get('page')

    restaurants=paginator.get_page(page_number)

    print(Restaurants)
    if request.user.is_authenticated:
        print("✅ User is logged in:", request.user)
    else:
        print("❌ User is not logged in")

    return render(request,"homepage/mainpage.html",{'Restaurant':restaurants})


