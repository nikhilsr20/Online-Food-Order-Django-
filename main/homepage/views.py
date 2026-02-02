from django.shortcuts import render
from partner.models import Restaurants
from django.http import JsonResponse
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
