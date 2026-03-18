from django.shortcuts import render,redirect
from partner.models import Restaurants
from django.http import JsonResponse
from django.core.paginator import Paginator
from cart.forms import Addressform
from partner.models import Restaurants,Item,Order,OrderItem
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import CurrAddress
from cart.models import DeliveryAddress

# Create your views here.
def home(request):

    addresses=DeliveryAddress.objects.all()
    form = Addressform()
    if request.method == 'POST' and 'newaddress' in request.POST:
        
        form = Addressform(request.POST)
        print(form)
        if form.is_valid():
            print("hello")

            x=form.save(commit=False)
            x.userr=request.user
            x.save()
            return redirect('home')

    Restaurant=Restaurants.objects.all()
   
    if request.GET.get('sort')=="deliverytime":
         Restaurant = Restaurant.order_by('deliverytime') 

    if request.GET.get('sort')=="rating":
         Restaurant = Restaurant.order_by('rating')    

    if request.GET.get('sort')=="default":
            Restaurant=Restaurants.objects.all()

    paginator=Paginator(Restaurant,6)

    page_number=request.GET.get('page')

    restaurants=paginator.get_page(page_number)

    return render(request,"homepage/mainpage.html",{'Restaurant':restaurants,'form':form,'addresses':addresses})

def search(request):

    query = request.GET.get("q")
    results = Restaurants.objects.filter(Name__icontains=query)

    data = []
    for r in results:
        data.append({
            "id": r.id,
            "Name": r.Name,
            "rating": r.rating,
            "deliverytime": r.deliverytime,
            "Cuisenetypes": r.Cuisenetypes,
            "Location": r.Location,
            "image": r.image.url if r.image else ""
        })
    return JsonResponse(data, safe=False)
