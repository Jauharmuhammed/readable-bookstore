
from django import forms
from .models import Category,SubCategory, Language

class CategoryCreationForm(forms.ModelForm):
  
  class Meta:
    model = Category
    fields = '__all__'

    widgets = {
              'category_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Category Name"}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Category Description", 'rows':4}),
          }

class SubCategoryCreationForm(forms.ModelForm):
  
  class Meta:
    model = SubCategory
    fields = '__all__'
    widgets = {
              'subcategory_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Sub-category Name"}),
              'category' : forms.Select(attrs={'id':"nameWithTitle", 'class':"form-control"}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Sub-category Description", 'rows':4}),
          }

class LanguageCreationForm(forms.ModelForm):
  
  class Meta:
    model = Language
    fields = '__all__'

    widgets = {
              'language_name': forms.TextInput(attrs={'id':"nameWithTitle", 'class':"form-control", 'placeholder':"Language Name"}),
              'description': forms.Textarea(attrs={'id':"descriptionWithTitle", 'class':"form-control", 'placeholder':"Language Description",'rows':4}),
          }