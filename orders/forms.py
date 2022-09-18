from pyexpat import model
from django import forms
from accounts.models import Address

class OrderForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['email', 'mobile', 'first_name', 'last_name', 'address', 'landmark', 'city', 'pin_code', 'state', 'country']