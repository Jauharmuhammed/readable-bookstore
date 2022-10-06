from pyexpat import model
from django import forms
from .models import Banner

class BannerForm(forms.ModelForm):

  class Meta:
    model = Banner
    fields = '__all__'

    widgets = {
      'banner_image' : forms.ClearableFileInput(attrs={'class':"form-control"}),
      'title': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Title"}),
      'tagline': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Tagline"}),
    }
