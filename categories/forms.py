
from django import forms
from .models import Category,SubCategory, Language

class CategoryCreationForm(forms.ModelForm):
  
  class Meta:
    model = Category
    fields = '__all__'

    widgets = {
              'category_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Category Name"}),
              'tagline': forms.Textarea(attrs={'id':"taglineWithTitle", 'class':"form-control", 'placeholder':"Category Tagline", 'rows':2}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Category Description", 'rows':4}),
          }

class SubCategoryCreationForm(forms.ModelForm):
  
  class Meta:
    model = SubCategory
    fields = '__all__'
    widgets = {
              'subcategory_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Sub-category Name"}),
              'category' : forms.Select(attrs={'id':"nameWithTitle", 'class':"form-control"}),
              'tagline': forms.Textarea(attrs={'id':"taglineWithTitle", 'class':"form-control", 'placeholder':"Category Tagline", 'rows':2}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Sub-category Description", 'rows':4}),
              'discount': forms.NumberInput(attrs={'id':"discountWithTitle", 'class':"form-control", 'placeholder':"Discount", 'max':99,}),
          }

class LanguageCreationForm(forms.ModelForm):
  
  class Meta:
    model = Language
    fields = '__all__'

    widgets = {
              'language_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Language Name"}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Language Description",'rows':4}),
          }