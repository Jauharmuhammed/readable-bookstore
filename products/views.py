
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from django.contrib import messages

from carts.models import CartItem
from carts.views import _cart_id

from .models import Products, Review
from .forms import ReviewForm
from categories.models import Category, SubCategory, Language
from orders.models import OrderProduct

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def products(request, category_slug=None, sub_category_slug= None):
  categories = None
  sub_categories = None
  products = None

  if category_slug is not None:
    if sub_category_slug is not None:
      sub_categories = get_object_or_404(SubCategory, slug=sub_category_slug)
      products = Products.objects.filter(sub_category=sub_categories, is_available=True).order_by('-modified_date')

      # You can also simpify using the oneline code below
      # products = Products.objects.filter(sub_category__slug=sub_category_slug)
    else:
      categories = get_object_or_404(Category, slug=category_slug)
      sub_categories = SubCategory.objects.filter(category=categories)
      products = Products.objects.filter(sub_category__in=sub_categories, is_available=True).order_by('-modified_date')


      # You can also simpify using the oneline code below
      # products = Products.objects.filter(sub_category__category__slug=category_slug)

  else:
    products = Products.objects.filter(is_available=True).order_by('-modified_date')

  if products is not None:
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
  else:
    paged_products = None

  product_count = products.count()

  context = {
    'products' : paged_products,
    'product_count': product_count,
  }
  return render(request, 'products/products.html', context)


def products_by_language(request, language_slug=None):
  language = None
  products = None

  if language_slug is not None:
      language = get_object_or_404(Language, slug=language_slug)
      products = Products.objects.filter(language=language, is_available=True).order_by('-modified_date')

  else:
    products = Products.objects.all().filter(is_available=True).order_by('-modified_date')

  product_count = products.count()

  if products is not None:
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
  else:
    paged_products = None

  context = {
    'products' : paged_products,
    'product_count': product_count,
  }
  return render(request, 'products/products.html', context)


def product_view(request, product_slug=None):
  product = Products.objects.get(slug=product_slug)

  in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()

  try:
      is_ordered=OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
  except:
      is_ordered=None

  try:
      is_already_reviewed=Review.objects.filter(user=request.user, product_id=product.id).exists()
  except:
      is_already_reviewed=None

  reviews = Review.objects.filter(product=product, status=True)
  context = {
    'product': product,
    'in_cart': in_cart,
    'is_ordered':is_ordered,
    'reviews':reviews,
    'is_already_reviewed':is_already_reviewed,
  }
  return render(request, 'products/product-view.html', context)


def search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword :
      products = Products.objects.filter(
          Q(name__icontains=keyword) | 
          Q(author__icontains=keyword) |
          Q(sub_category__subcategory_name__icontains=keyword) |
          Q(sub_category__category__category_name__iexact=keyword) |
          Q(language__language_name__iexact=keyword)
        ).order_by('-modified_date')
      product_count = products.count()

      paginator = Paginator(products, 8)
      page = request.GET.get('page')
      paged_products = paginator.get_page(page)

    else:
      products = None
      product_count = 0
      paged_products = None

  
  context = {
    'products' : paged_products ,
    'product_count': product_count,
    'keyword' : keyword
  }
  return render(request, 'products/products.html', context)


def review(request,product_id):
  url=request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      existing_review=Review.objects.get(user__id=request.user.id, product__id=product_id)
      form=ReviewForm(request.POST, instance=existing_review)
      form.save()
      messages.success(request,'Thank You ! Your review has been updated')
      return redirect(url)
    except Review.DoesNotExist:
      form=ReviewForm(request.POST)
      if form.is_valid():
        data=Review()
        data.title=form.cleaned_data['title']
        data.rating=form.cleaned_data['rating']
        data.review=form.cleaned_data['review']
        data.ip=request.META.get('REMOTE_ADDR')
        data.product_id=product_id
        data.user_id=request.user.id
        data.save()
        messages.success(request,'Thank You ! Your review has been Saved')
        return redirect(url)


def delete_review(request, product_id):
  url=request.META.get('HTTP_REFERER')
  try:
    del_review = Review.objects.get(user=request.user, product_id=product_id)
  except:
    pass
  if del_review is not None:
    del_review.delete()
    messages.success(request,'Your review is deleted successfully')
    return redirect(url)
  else:
    return redirect(url)




