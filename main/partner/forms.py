from django import forms
from django.forms import ModelForm
from .models import PartnerSignup


class PartnerSignupForm(ModelForm):
    class Meta:
        model = PartnerSignup
        fields = "__all__" 
        widgets = {
        'phone': forms.TextInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Enter your Mobile number'
         }),
        'password': forms.PasswordInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Enter password'
        }),
        'confirmpass': forms.PasswordInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Confirm password'
        })
    }
    
    def clean_phone(self):
        phone=self.cleaned_data.get('phone')

        if not str(phone).isdigit():
            raise forms.ValidationError("Phone number must contain digits")
        
        if len(str(phone))!=10:
            raise forms.ValidationError("phone number must be of 10 digits")
        
        return phone
    
    def clean_confirmpass(self):
        password=self.cleaned_data.get('password')
        check=self.cleaned_data.get('confirmpass')

        if password!=check:
            raise forms.ValidationError('passwords does not match')
        
        return check
    

class PartnerLoginForm(ModelForm):
    class Meta:
        model = PartnerSignup
        fields = ['phone','password'] 
        widgets = {
        'phone': forms.TextInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Enter your Mobile number'
         }),
        'password': forms.PasswordInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Enter password'
        })
    }
    
    def clean_phone(self):
        phone=self.cleaned_data.get('phone')

        if not str(phone).isdigit():
            raise forms.ValidationError("Phone number must contain digits")
        
        if len(str(phone))!=10:
            raise forms.ValidationError("phone number must be of 10 digits")
        
        if not  PartnerSignup.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This is not a valid user")
        return phone
    
    def clean_password(self):
        password=self.cleaned_data.get('password')
        phone=self.cleaned_data.get('phone')
        user = PartnerSignup.objects.filter(phone=phone).first()
        if user is not None:
            if user.password!=password:
                raise forms.ValidationError("The password is wrong")
                 
            
            
        
        return password  