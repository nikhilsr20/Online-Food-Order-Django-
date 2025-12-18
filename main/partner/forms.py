from django import forms
from django.forms import ModelForm
from .models import PartnerSignup,Restaurants,Category,Item


class RestaurantsForm(ModelForm):

    class Meta:
        model=Restaurants
        fields= "__all__"
        widgets = {
        'Name': forms.TextInput(attrs={'class': 'Restaurant-name', 'placeholder': "Enter Restaurant Name"}),
        'Restauranttype': forms.Select(attrs={'class': 'Restaurant-type', 'placeholder': "Enter Restaurant Type"}),
        'Cuisenetypes': forms.TextInput(attrs={'class': 'Restaurant-cuisines', 'placeholder':"Enter Restaurant cuisines"}),
        'description': forms.Textarea(attrs={'class':'Restaurant-description','placeholder':"Enter Restaurant Description"}),
        'image': forms.FileInput(attrs={'class':'Restaurant-img'}),
        'Location': forms.TextInput(attrs={
                'class': 'Restaurant-location',
                'placeholder': "Enter Full Location"
            }),
        'city': forms.TextInput(attrs={
                 'class': 'Restaurant-location',
                'placeholder': "Enter City Name"
            }),
        'state': forms.TextInput(attrs={
                'class': 'Restaurant-location',
                'placeholder': "Enter State Name"
            }),
        'pincode': forms.TextInput(attrs={
                'class': 'Restaurant-location',
                'placeholder': "Enter Pincode"
            }),

       
        'rating': forms.NumberInput(attrs={
                'class': 'Restaurant-rating',
                'placeholder': "Rating (0 to 5)",
                'step': "0.1",
                'min': "0",
                'max': "5"
            }),
         'deliverytime': forms.NumberInput(attrs={
                'class': 'Restaurant-time',
                'placeholder': "Delivery time in minutes"
            }),

        
        'Timeopen': forms.TimeInput(attrs={
                'class': 'Restaurant-time',
                'type': 'time'
            }),
        'Closetime': forms.TimeInput(attrs={
                'class': 'Restaurant-time',
                'type': 'time'
            }),


        'Isopen': forms.CheckboxInput(attrs={
                'class': 'Restaurant-time'
            }),
        }



    



class PartnerSignupForm(ModelForm):
    class Meta:
        model = PartnerSignup
        fields = "__all__" 
        widgets = {
        'username': forms.TextInput(attrs={
        'class': 'partner-login-input',
        'placeholder': 'Enter username'
         }),    
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
    

class CategoryForm(ModelForm):
   
    class Meta:
        model=Category
        fields="__all__"
        widgets={
            'name':forms.TextInput(attrs={'class':'partner-add-category-div-elem2','placeholder':"enter a category"})
        }
