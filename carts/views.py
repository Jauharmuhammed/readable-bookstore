from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Address

from products.models import Products, Variation, Wishlist
from .models import Cart, CartItem

from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    car_id = request.session.create()
  return cart_id

def add_to_cart(request, product_id):
  url=request.META.get('HTTP_REFERER')
  user = request.user
  product = Products.objects.get(id=product_id)
  if user.is_authenticated:
    product_variation=[]
    if request.method == 'POST':
      for item in request.POST:
        key = item
        value =  request.POST[key]
        
        try:
            variation = Variation.objects.get(product=product, variation_value__iexact=value)
            product_variation.append(variation)
        except:
            pass
      
      try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
      except Cart.DoesNotExist:
        cart = Cart.objects.create(
          cart_id = _cart_id(request)
        )
      cart.save()

      is_cart_item_exists = CartItem.objects.filter(product=product, user=user).exists()
      if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, user=user)
        existing_variation_list = []
        id = []
        for item in cart_item:
          existing_variation = item.variation.all()
          existing_variation_list.append(list(existing_variation))
          id.append(item.id)

        print(product_variation)
        print(existing_variation_list)

        if product_variation in existing_variation_list:
          index = existing_variation_list.index(product_variation)
          item_id = id[index]
          item = CartItem.objects.get(product=product, id=item_id)
          item.quantity += 1
          item.save()

        else:
          item = CartItem.objects.create(product=product, quantity=1, user=user)
          item.variation.clear()
          item.variation.add(*product_variation)
          item.save()


          
      else:
        cart_item = CartItem.objects.create(
          product = product,
          cart = cart,
          quantity = 1,
          user = user
        )
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
        cart_item.save()

  else:

    product_variation=[]
    if request.method == 'POST':
      for item in request.POST:
        key = item
        value =  request.POST[key]
        
        try:
            variation = Variation.objects.get(product=product, variation_value__iexact=value)
            product_variation.append(variation)
        except:
            pass
      
      try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
      except Cart.DoesNotExist:
        cart = Cart.objects.create(
          cart_id = _cart_id(request)
        )
      cart.save()

      is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
      if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variation_list = []
        id = []
        for item in cart_item:
          existing_variation = item.variation.all()
          existing_variation_list.append(list(existing_variation))
          id.append(item.id)

        print(product_variation)
        print(existing_variation_list)

        if product_variation in existing_variation_list:
          index = existing_variation_list.index(product_variation)
          item_id = id[index]
          item = CartItem.objects.get(product=product, id=item_id)
          item.quantity += 1
          item.save()


        else:
          item = CartItem.objects.create(product=product, quantity=1, cart=cart)
          item.variation.clear()
          item.variation.add(*product_variation)
          item.save()


          
      else:
        cart_item = CartItem.objects.create(
          product = product,
          cart = cart,
          quantity = 1,
        )
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
        cart_item.save()
    
  return redirect(url)


    

def remove_from_cart(request, product_id, cart_item_id):
  product = get_object_or_404(Products, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1 :
      cart_item.quantity -= 1
      cart_item.save()
  except:
    pass
  return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
  product = get_object_or_404(Products, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)
    cart_item.delete()
  except:
    pass
  return redirect('cart')


def cart(request, cart_items=None, sub_total=0, total=0, shipping_charge = 0, quantity=0):
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active =True).order_by('-created_date')

    for cart_item in cart_items:
      sub_total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity


    if sub_total < 499:
      shipping_charge = 99
    total = sub_total + shipping_charge
  except ObjectDoesNotExist:
    pass

  context = {
    'cart_items' : cart_items,
    'sub_total': sub_total,
    'shipping_charge': shipping_charge,
    'total' : total,
    'quantity' : quantity
  }
  return render(request, 'products/cart.html', context)



@login_required(login_url='login')
def move_to_wishlist(request, product_id, cart_item_id):
  product = get_object_or_404(Products, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

      in_wishlist = Wishlist.objects.filter(user=request.user, product_id= product_id).exists()
      if in_wishlist:
        pass
      else:
        Wishlist.objects.create(
          user = request.user,
          product_id = product_id
        )
    else:
      return redirect('login')
    cart_item.delete()
    messages.success(request,'Item is moved to your wishlist')
  except:
    pass
  return redirect('cart')


@login_required(login_url='login')
def checkout(request, cart_items=None, sub_total=0, total=0, shipping_charge = 0, quantity=0):
  try:
    cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
    for cart_item in cart_items:
      sub_total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity


    if sub_total < 499:
      shipping_charge = 99
    total = sub_total + shipping_charge

    addresses = Address.objects.filter(user=request.user, is_active=True).order_by('-date_added')
  except ObjectDoesNotExist:
    pass

  context = {
    'cart_items' : cart_items,
    'sub_total': sub_total,
    'shipping_charge': shipping_charge,
    'total' : total,
    'quantity' : quantity,
    'addresses': addresses
  }
  return render(request, 'products/checkout.html', context)