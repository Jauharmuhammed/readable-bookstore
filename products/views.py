from django.shortcuts import render, get_object_or_404

from .models import Products
from categories.models import Category, SubCategory, Language

def products(request, category_slug=None, sub_category_slug= None):
  categories = None
  sub_categories = None
  products = None

  if category_slug is not None:
    if sub_category_slug is not None:
      sub_categories = get_object_or_404(SubCategory, slug=sub_category_slug)
      products = Products.objects.filter(sub_category=sub_categories, is_available=True)

      # You can also simpify using the oneline code below
      # products = Products.objects.filter(sub_category__slug=sub_category_slug)
    else:
      categories = get_object_or_404(Category, slug=category_slug)
      sub_categories = SubCategory.objects.filter(category=categories)
      products = Products.objects.filter(sub_category__in=sub_categories, is_available=True)


      # You can also simpify using the oneline code below
      # products = Products.objects.filter(sub_category__category__slug=category_slug)

  else:
    products = Products.objects.all().filter(is_available=True)


  context = {
    'products' : products
  }
  return render(request, 'products/products.html', context)


def products_by_language(request, language_slug=None):
  language = None
  products = None

  if language_slug is not None:
      language = get_object_or_404(Language, slug=language_slug)
      products = Products.objects.filter(language=language, is_available=True)

  else:
    products = Products.objects.all().filter(is_available=True)

  context = {
    'products' : products
  }
  return render(request, 'products/products.html', context)


def product_view(request, product_slug=None):
  product = Products.objects.get(slug=product_slug)

  context = {
    'product': product
  }
  return render(request, 'products/product-view.html', context)