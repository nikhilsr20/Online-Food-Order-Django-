from django.urls import path
from . import views

urlpatterns=[
   path('res/<int:id>/',views.restaurant)
]