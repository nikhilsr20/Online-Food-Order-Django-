from django import forms
from .models import DeliveryAddress
from django.forms import ModelForm



class Addressform(ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
        exclude = ['userr'] 
        widgets = {
            'Address': forms.TextInput(attrs={'class': 'Addnewaddress-page-inputs-div1-input1'}),
            'Flat': forms.TextInput(attrs={'class': 'Addnewaddress-page-inputs-div1-input2'}),
            'Landmark': forms.TextInput(attrs={'class': 'Addnewaddress-page-inputs-div1-input3'}),
            'head': forms.TextInput(attrs={'class': 'Addnewaddress-page-inputs-div4-input'}),
        }




