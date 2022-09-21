from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from orders.models import Address
from .models import CustomUser, UserProfile




class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'password', 'mobile_number')


    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' ','class': 'form-control',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' ','class': 'form-control ',}),required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': ' ','class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ' ','class': 'form-control password',}),validators=[validate_password])
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' ','class': 'form-control','maxlength':"10", 'pattern':"\d{10}", 'title':"Please enter exactly 10 digits", }))
    

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['email', 'mobile', 'first_name', 'last_name', 'address', 'landmark', 'city', 'pin_code', 'state', 'country']
 

class UserForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ['first_name', 'last_name', 'mobile_number']

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ['profile_picture', 'date_of_birth', 'location']


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = '__all__'

    