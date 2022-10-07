from pyexpat import model
from django import forms
from accounts.models import Address
from orders.models import Coupon

class OrderForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['email', 'mobile', 'first_name', 'last_name', 'address', 'landmark', 'city', 'pin_code', 'state', 'country']

class CouponForm(forms.ModelForm):
  class Meta:
    model = Coupon
    fields = '__all__'