from django.urls import path
from . import views
urlpatterns = [
   path('cart/',views.cart,name='cart'),
   path('track/',views.track,name='trackorder'),
   path('cartpartial/',views.update_my_cart,name='update_my_cart'),
    path('achange/',views.achange,name='achange'),
   
]
