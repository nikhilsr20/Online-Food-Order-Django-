from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='partner'),
    path('main/',views.main,name='partner-main'),
     path('login/',views.login,name='partnerlogin'),
      path('logout/',views.login,name='partnerlogout'),

]
