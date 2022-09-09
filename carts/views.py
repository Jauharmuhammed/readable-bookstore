from django.shortcuts import render, redirect, get_object_or_404

from products.models import Products
from .models import Cart, CartItem

from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    car_id = request.session.create()
  return cart_id

def add_to_cart(request, product_id):
  product = Products.objects.get(id=product_id)
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id = _cart_id(request)
    )
  cart.save()

  try:
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
  except:
    cart_item = CartItem.objects.create(
      product = product,
      cart = cart,
      quantity = 1
    )
    cart_item.save()
  
  return redirect('cart')

def remove_from_cart(request, product_id):
  cart = Cart.objects.get(cart_id = _cart_id(request))
  product = get_object_or_404(Products, id=product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  if cart_item.quantity > 1 :
    cart_item.quantity -= 1
    cart_item.save()
  return redirect('cart')

def remove_cart_item(request, product_id):
  cart = Cart.objects.get(cart_id = _cart_id(request))
  product = get_object_or_404(Products, id=product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  cart_item.delete()
  return redirect('cart')


def cart(request, cart_items=None, total=0):
  try:
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active =True).order_by('-modified_time')
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
  except ObjectDoesNotExist:
    pass

  context = {
    'cart_items' : cart_items,
    'total' : total
  }
  return render(request, 'products/cart.html', context)
