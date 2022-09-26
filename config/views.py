from django.shortcuts import redirect, render
from categories.models import SubCategory

from products.models import Products


def home(request):
    slide_products = Products.objects.all().order_by('-create_date')[:5]
    display_categories = SubCategory.objects.filter()[:5]
    choice_of_the_week = Products.objects.filter(name__icontains= 'forty rules of love').first()
    context = {
      'slide_products':slide_products,
      'display_categories':display_categories,
      'choice_of_the_week':choice_of_the_week,
    }
    return render(request, 'index.html', context)