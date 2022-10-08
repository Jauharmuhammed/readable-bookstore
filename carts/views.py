import imp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Address
from orders.models import Coupon

from products.models import Products, Variation, Wishlist
from .models import Cart, CartItem, ShippingCharge

from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse


def _cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    car_id = request.session.create()
  return cart_id



def cart(request, cart_items=None, sub_total=0, sub_total_mrp=0, discount_mrp=0, total=0, shipping_cost = 0, quantity=0):
  if 'coupon_id' in request.session:
    del request.session['coupon_id']

  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active =True).order_by('-created_date')

    for cart_item in cart_items:
      sub_total += cart_item.item_total()
      sub_total_mrp += cart_item.item_total_mrp()
      quantity += cart_item.quantity

    discount_mrp= sub_total_mrp - sub_total

    shipping_charge = ShippingCharge.objects.first()
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    total = sub_total + shipping_cost

    out_of_stock_item = None
    for cart_item in cart_items:
      if cart_item.quantity > cart_item.product.stock:
        out_of_stock_item = True
        break
        
  except ObjectDoesNotExist:
    out_of_stock_item = None

  context = {
    'cart_items' : cart_items,
    'sub_total': sub_total,
    'sub_total_mrp':sub_total_mrp,
    'discount_mrp':discount_mrp,
    'shipping_charge': shipping_cost,
    'total' : total,
    'quantity' : quantity,
    'out_of_stock_item':out_of_stock_item
  }
  return render(request, 'products/cart.html', context)


def add_to_cart(request, product_id):
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
          messages.success(request, 'Item added to your cart')


          
      else:
        cart_item = CartItem.objects.create(
          product = product,
          quantity = 1,
          user = user
        )
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
        cart_item.save()
        messages.success(request, 'Item added to your cart')


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
          messages.success(request, 'Item added to your cart')


          
      else:
        cart_item = CartItem.objects.create(
          product = product,
          cart = cart,
          quantity = 1,
        )
        cart_item.variation.clear()
        cart_item.variation.add(*product_variation)
        cart_item.save()
        messages.success(request, 'Item added to your cart')

      
  return JsonResponse({ 'message': 'Item added to cart successfull'})


    

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
    messages.success(request, 'Item removed from your cart')
  except:
    pass
  return redirect('cart')



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
def checkout(request, cart_items=None, sub_total=0, sub_total_mrp=0, shipping_cost=0, discount_mrp=0, total=0, shipping_charge = 0, quantity=0, coupon_discount=0):
  try:
    cart_items = CartItem.objects.filter(user=request.user, is_active =True).order_by('-created_date')
    for cart_item in cart_items:
      sub_total += cart_item.item_total()
      sub_total_mrp += cart_item.item_total_mrp()
      quantity += cart_item.quantity

    discount_mrp= sub_total_mrp - sub_total

    shipping_charge = ShippingCharge.objects.first()
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    if 'coupon_id' in request.session:
      coupon_id = request.session['coupon_id']
      coupon_discount_percentage= Coupon.objects.get(id = coupon_id).coupon_discount
      coupon_discount = sub_total * int(coupon_discount_percentage) / 100
      sub_total = sub_total - coupon_discount

    total = sub_total + shipping_cost
  
    addresses = Address.objects.filter(user=request.user, is_active=True).order_by('-date_added')
  except ObjectDoesNotExist:
    pass

  context = {
    'cart_items' : cart_items,
    'sub_total': sub_total,
    'sub_total_mrp':sub_total_mrp,
    'discount_mrp':discount_mrp,
    'coupon_discount': round(coupon_discount),
    'shipping_charge': shipping_cost,
    'total' : round(total),
    'quantity' : quantity,
    'addresses': addresses
  }
  return render(request, 'products/checkout.html', context)