from django import forms
from .models import Products, Review, Variation

class ProductCreationForm(forms.ModelForm):

    class Meta:
      model = Products
      fields = '__all__'

      widgets = {
              'name': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Title"}),
              'isbn': forms.TextInput(attrs={'class':"form-control", 'placeholder':"ISBN"}),
              'sub_category': forms.Select(attrs={'class':"form-select",'aria-label':"Choose Sub-category"}),
              'language': forms.Select(attrs={'class':"form-select", 'aria-label':"Choose Language"}),

              'author': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Author"}),
              'Publisher': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Publisher"}),
              'release_date': forms.DateInput(attrs={'class':"form-control", 'type':"date", 'value':"YYYY-MM-DD", 'id':"html5-date-input"}),
              'price': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Price", 'min':'0',}),
              'discount': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Discount", 'min':'0','max':'99'}),
              'stock': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Stock", 'min':'0'}),
              'is_available': forms.CheckboxInput(),

              'cover_image' : forms.ClearableFileInput(),
              'image1' : forms.ClearableFileInput(),
              'image2' : forms.ClearableFileInput(),
              'image3' : forms.ClearableFileInput(),

              'description': forms.Textarea(attrs={'class':"form-control", 'placeholder':"Product Description" }),

              'number_of_pages': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Number of Pages"}),
              'weight': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Weight"}),
              'height': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Height"}),
              'width': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Width"}),
              'spine_width': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Spine width"}),

          }


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['title','review','rating',]
