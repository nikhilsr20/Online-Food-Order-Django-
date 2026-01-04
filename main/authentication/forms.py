from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import Cart


class Register(UserCreationForm):
    username=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'register-username'}))
    password1=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'register-password1','placeholder':'Enter password'}))
    password2=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'register-password2','placeholder':'Confirm password'}))

    first_name=forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'register-first_name'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
               'email':forms.TextInput(attrs={'class':'register-email'}),
               'first_name':forms.TextInput(attrs={'class':'register-first_name'}),
               'last_name':forms.TextInput(attrs={'class':'register-last_name'}),

        }
    
    def clean_email(self):
        data=self.cleaned_data.get('email')
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already registered")
        
        if "gmail.com" not in data:
          raise forms.ValidationError("Email must be a Gmail address.")
        
        return data
    def clean(self):
        cleaned_data=super().clean()
        p1=cleaned_data.get('password1')
        p2=cleaned_data.get('password2')

        if p1!=p2:
            raise forms.ValidationError("password does not match")


class Login(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'login-email', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'login-password', 'placeholder': 'Enter your password'})
    )
    
   
    def clean_email(self):
        data=self.cleaned_data.get('username')

        
        if "gmail.com" not in data:
          raise forms.ValidationError("Email must be a Gmail address.")
        
        return data
    
    def clean(self):
         username = self.cleaned_data.get('username')
         password1 = self.cleaned_data.get('password')

         try:
            user = User.objects.get(email=username)
          
         except User.DoesNotExist:
            raise forms.ValidationError("user does not found with this email")
  
         if not user.check_password(password1):
            raise forms.ValidationError("Incorrect Password")

         self.user_cache = user  
        

         return self.cleaned_data
         

   
        
# class Cart_form(forms.ModelForm):

#     class Meta:
#         model=Cart
#         exclude=['user']
#         widgets = {
#             'item': forms.TextInput(attrs={'class': 'not'}),
#             'food_type': forms.TextInput(attrs={'class': 'not'}),
#             'quantity': forms.NumberInput(attrs={'class': 'not'}),
#             'price': forms.NumberInput(attrs={'class': 'not'}),
#         }
