from django.urls import path
from . import views

urlpatterns=[
   path('res/<int:id>/',views.restaurant),
   path('resupdate/',views.update_cart,name='update_cart')
]