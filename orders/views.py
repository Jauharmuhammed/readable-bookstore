from django.shortcuts import render, redirect
from accounts.models import Address
from products.models import Products, Variation

from django.contrib import messages

from carts.models import CartItem, ShippingCharge
from orders.models import Coupon, CouponCheck, Order, OrderDetails, Payment, OrderProduct, ShippingMethod
from .forms import OrderForm

import datetime
from django.http import JsonResponse, HttpResponse

import string
import random

from django.core.mail import send_mail
from django.template.loader import render_to_string



def unique_id(size):
    chars = list(set(string.ascii_letters))
    return ''.join(random.choices(chars, k=size))

def applyCoupon(request):
  coupon_code = request.GET['coupon_code']
  print(coupon_code)

  if 'coupon_id' in request.session:
    del request.session['coupon_id']
    
  is_coupon_code_exists = Coupon.objects.filter(coupon_code= coupon_code).exists()
  if is_coupon_code_exists:
    coupon_id = Coupon.objects.get(coupon_code=coupon_code).id
    is_expired = CouponCheck.objects.filter(user=request.user, coupon=coupon_id).exists()
    if is_expired:
      messages.error(request, 'Coupon is already used!')
      return JsonResponse({ 'message':'Coupon is already used!'})
    else:
      coupon = Coupon.objects.get(coupon_code= coupon_code)
      discount_percentage = coupon.coupon_discount
      request.session['coupon_id'] = coupon_id
      messages.success(request, 'Coupon Applied successfully')
      return JsonResponse( { 'discount_percentage': discount_percentage})

  else:
    messages.error(request, 'Coupon does not exists!')
    return JsonResponse({'message':'Coupon does not exists!'})


def save_address(request, sub_total=0, total=0, sub_total_mrp=0, shipping_cost=0, discount_mrp=0, shipping_charge = 0, quantity=0, coupon_discount=0):
  current_user = request.user
  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      data = Address()
      data.user = current_user
      data.email = form.cleaned_data['email']
      data.mobile = form.cleaned_data['mobile']
      data.first_name = form.cleaned_data['first_name']
      data.last_name = form.cleaned_data['last_name']
      data.address = form.cleaned_data['address']
      data.landmark = form.cleaned_data['landmark']
      data.city = form.cleaned_data['city']
      data.pin_code = form.cleaned_data['pin_code']
      data.state = form.cleaned_data['state']
      data.country = form.cleaned_data['country']

      address = None
      existing_addresses = Address.objects.filter(user=current_user).order_by('-date_added')
      if existing_addresses is not None:
        for existing_address in existing_addresses:
          if data.__equal__(existing_address):
            print('Found Address in Existing address list')
            address = existing_address
            break

        if address is None:
          print('saved as a new address')
          data.save()
          address = Address.objects.get(user=current_user, id= data.id)
      else:
        print('none')
        data.save()


    addresses = Address.objects.filter(user=current_user, is_active=True).order_by('-date_added')

    cart_items = CartItem.objects.filter(user=current_user)
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


    context = {
      'cart_items' : cart_items,
      'addresses': addresses,
      'sub_total': sub_total,
      'sub_total_mrp':sub_total_mrp,
      'discount_mrp': round(discount_mrp),
      'coupon_discount': round(coupon_discount),
      'shipping_charge': shipping_cost,
      'total' : round(total),
      'quantity' : quantity
    }
    return render(request, 'orders/select-address.html', context)

  else:
    return redirect('checkout')




def shipping_method(request, sub_total=0, total=0, sub_total_mrp=0, shipping_cost=0, discount_mrp=0, shipping_charge = 0, quantity=0, coupon_discount=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')

  if request.method == "POST":
    
    address_id = request.POST.get('address')
    request.session['address_id'] = address_id

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

      request.session['coupon_discount'] = round(coupon_discount)
      # del request.session['coupon_id']
    
    elif 'coupon_discount' in request.session:
      coupon_discount = request.session['coupon_discount']
      sub_total = sub_total - coupon_discount




    total = sub_total + shipping_cost

    address = Address.objects.get(user=current_user, id=int(address_id))

    shipping_methods = ShippingMethod.objects.all()

    context = {
      'cart_items' : cart_items,
      'address': address,
      'sub_total': round(sub_total),
      'sub_total_mrp': round(sub_total_mrp),
      'discount_mrp': round(discount_mrp),
      'coupon_discount': round(coupon_discount),
      'shipping_charge': round(shipping_cost),
      'shipping_methods': shipping_methods,
      'total' : round(total),
      'quantity' : quantity
    }
    return render(request, 'orders/shipping.html', context)


def payment_method(request, sub_total=0, total=0, sub_total_mrp=0, shipping_cost=0, discount_mrp=0, shipping_charge = 0, quantity=0, coupon_discount=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')

  if request.method == "POST":
    shipping_method = request.POST['shipping-method']
    address_id = request.session['address_id']

    for cart_item in cart_items:
      sub_total += cart_item.item_total()
      sub_total_mrp += cart_item.item_total_mrp()
      quantity += cart_item.quantity

    discount_mrp= sub_total_mrp - sub_total

    shipping_charge = ShippingCharge.objects.first()
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    shipping_method_choosed = ShippingMethod.objects.get(shipping_method=shipping_method)
    shipping_charge = shipping_method_choosed.charge

    request.session['shipping_method_id'] = shipping_method_choosed.id

    if 'coupon_discount' in request.session:
      coupon_discount = request.session['coupon_discount']
      sub_total = sub_total - coupon_discount

    total_shipping_charge = shipping_cost + shipping_charge

    total = sub_total + total_shipping_charge

    address = Address.objects.get(user=current_user, id=int(address_id))


    context = {
      'cart_items' : cart_items,
      'address': address,
      'sub_total': round(sub_total),
      'sub_total_mrp': round(sub_total_mrp),
      'discount_mrp': round(discount_mrp),
      'coupon_discount': round(coupon_discount),
      'shipping_charge': round(shipping_cost),
      'shipping_method': shipping_method_choosed,
      'total_shipping_charge': round(total_shipping_charge),
      'total' : round(total),
      'quantity' : quantity
    }

    return render(request, 'orders/payment-method.html', context)




def place_order(request, sub_total=0, total=0, sub_total_mrp=0, shipping_cost=0, discount_mrp=0, shipping_charge = 0, quantity=0, coupon_discount=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')

  if request.method == "POST":
    shipping_method_id = request.session['shipping_method_id']
    address_id = request.session['address_id']

    payment_method = request.POST['payment-method']

    for cart_item in cart_items:
      sub_total += cart_item.item_total()
      sub_total_mrp += cart_item.item_total_mrp()
      quantity += cart_item.quantity

    discount_mrp= sub_total_mrp - sub_total

    shipping_charge = ShippingCharge.objects.first()
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    shipping_method_choosed = ShippingMethod.objects.get(id=shipping_method_id)
    shipping_charge = shipping_method_choosed.charge


    if 'coupon_discount' in request.session:
      coupon_discount = request.session['coupon_discount']
      sub_total = sub_total - coupon_discount

    total_shipping_charge = shipping_cost + shipping_charge

    total = sub_total + total_shipping_charge

    data = Order()

    ip_address = request.META.get('REMOTE_ADDR')
    address = Address.objects.get(user=current_user, id=int(address_id))


    data.user = current_user
    data.gross_amount = sub_total_mrp
    data.discount = discount_mrp
    data.coupon_discount = coupon_discount
    data.shipping_charge = total_shipping_charge
    data.order_total = total
    data.address = address
    data.ip= ip_address
    data.shipping_method = shipping_method_choosed
    data.save()

    # ORDER_ID 
    yr=int(datetime.date.today().strftime('%Y'))
    dt=int(datetime.date.today().strftime('%d'))
    mt=int(datetime.date.today().strftime('%m'))
    d=datetime.date(yr,mt,dt)
    current_date=d.strftime("%Y%m%d")
    order_id= str('OD000RBS') + current_date + str(data.id)
    data.order_id=order_id
    data.save()
    print(order_id)
    
    order = Order.objects.get(user=current_user, is_ordered=False, order_id=order_id)

    request.session['order_id'] = order_id


    if payment_method == 'payOnDelivery':
      
      order.is_ordered = True
      payment= Payment()
      payment.payment_method = payment_method
      payment.user = current_user
      payment.amount = total

      # payment id payOnDelivery
      id =str(order.id)
      id_len=len(id)
      unique_id_generated = unique_id(11-id_len)
      payment_id= str('pay_Pod') + str(unique_id_generated) + id

      payment.payment_id=payment_id
      payment.status = 'Pending'
      payment.save()

      order.payment = payment
      order.status = 'Placed'
      order.save()

      order_products=[]
      for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order = order
        orderproduct.payment=payment
        orderproduct.user=request.user
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        orderproduct.price=item.product.price
        orderproduct.offer_price=item.product.offer_price()
        orderproduct.gross_amount=item.item_total_mrp()
        orderproduct.discount=item.item_discount()
        orderproduct.total=item.item_total()
        orderproduct.is_ordered=True
        orderproduct.save()

        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variation.all()
        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        order_products.append(orderproduct.product.name)
        
        #reduce the quantity of ordered product from stock
        product = Products.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

      #clear the cart items of the user
      CartItem.objects.filter(user=current_user).delete()

      # create order date object for the order
      OrderDetails.objects.create(
        order = order,
        order_status = order.status,
      )

      # delete data from session
      if request.session['order_id']:
        del request.session['order_id']
        del request.session['address_id']
        del request.session['shipping_method_id']
        
      if 'coupon_discount' in request.session:
        del request.session['coupon_discount']

      if 'coupon_id' in  request.session:
        coupon_id =  request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CouponCheck.objects.create(
          user= request.user,
          coupon = coupon,
        )
        del request.session['coupon_id']
      



      # Send order recieved email to to the customer
      mail_subject = 'Your order has been successfully placed'
      message = render_to_string('orders/order-received-email-pod.html',{
          'user' : request.user,
          'product': order_products,
          'amount': order.order_total,
          'address': address,
          'order_id': order.order_id,
          'order_date':order.updated_date,
      })
      to_email = request.user.email
      send_mail(mail_subject, message, 'readablebookstore@gmail.com', [to_email], fail_silently=False)

      return redirect('/orders/order-success/' +'?order_id='+order.order_id)

    elif payment_method == 'razorpay':

      context = {
        'cart_items' : cart_items,
        'address': address,
        'sub_total': round(sub_total),
        'sub_total_mrp': round(sub_total_mrp),
        'discount_mrp': round(discount_mrp),
        'coupon_discount': round(coupon_discount),
        'shipping_charge': round(shipping_cost),
        'shipping_method': shipping_method_choosed,
        'total_shipping_charge': round(total_shipping_charge),
        'total' : round(total),
        'quantity' : quantity
      }

      return render(request, 'orders/payment.html', context)


def razorpay_pay_now(request):
  order_id = request.session['order_id']
  order = Order.objects.get(user=request.user, order_id=order_id)
  payment_method = 'razorpay'
  return JsonResponse({
    'total': order.order_total,
    'full_name' : order.address.first_name + ' ' + order.address.last_name,
    'email': order.address.email,
    'mobile': order.address.mobile,
    'order_id': order.order_id,
    'payment_method': payment_method,
  })


def payment(request):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  for cart_item in cart_items:
    if cart_item.quantity > cart_item.product.stock:
      out_of_stock = True
      break
    else:
      out_of_stock = False
  if cart_items_count <= 0 or out_of_stock:
    return redirect('cart')

  order_id = request.session['order_id']
  order = Order.objects.get(user=current_user, order_id=order_id)
  if request.method == 'POST':
    payment_method = request.POST['payment_method']
    payment_id = request.POST.get('payment_id')
    amount = request.POST['payment_amount']

    order.is_ordered = True
    payment= Payment()
    payment.payment_method = payment_method
    payment.user = current_user
    payment.amount = amount

    payment.payment_id= payment_id
    payment.status = 'Successful'

    payment.save()

    order.payment = payment
    order.status = 'Placed'
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)

    order_products=[]
    for item in cart_items:
      orderproduct=OrderProduct()
      orderproduct.order = order
      orderproduct.payment=payment
      orderproduct.user=current_user
      orderproduct.product=item.product
      orderproduct.quantity=item.quantity
      orderproduct.price=item.product.price
      orderproduct.offer_price=item.product.offer_price()
      orderproduct.gross_amount=item.item_total_mrp()
      orderproduct.discount=item.item_discount()
      orderproduct.total=item.item_total()
      orderproduct.is_ordered=True
      orderproduct.save()

      cart_item=CartItem.objects.get(id=item.id)
      product_variation=cart_item.variation.all()
      orderproduct=OrderProduct.objects.get(id=orderproduct.id)
      orderproduct.variation.set(product_variation)
      orderproduct.save()

      order_products.append(orderproduct.product.name)
      
      #reduce the quantity of ordered product from stock
      product = Products.objects.get(id=item.product_id)
      product.stock -= item.quantity
      product.save()

    #clear the cart items of the user
    CartItem.objects.filter(user=current_user).delete()

    # create order date object for the order
    OrderDetails.objects.create(
      order = order,
      order_status = order.status,
    )


    # delete data from session
    if order_id in request.session:
      del request.session['order_id']
      del request.session['address_id']
      del request.session['shipping_method_id']

    if 'coupon_discount' in request.session:
      del request.session['coupon_discount']


    # create a coupen check object that helpes to evaluate the coupon status
    if 'coupon_id' in  request.session:
        coupon_id =  request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        CouponCheck.objects.create(
          user= request.user,
          coupon = coupon,
        )
        del request.session['coupon_id']


    # Send order recieved email to to the customer
    mail_subject = 'Your order has been successfully placed'
    message = render_to_string('orders/order-received-email-prepaid.html',{
        'user' : current_user,
        'product': order_products,
        'amount': order.order_total,
        'payment_id':payment_id,
        'address': order.address,
        'order_id': order.order_id,
        'order_date':order.updated_date,
    })
    to_email = current_user.email
    send_mail(mail_subject, message, 'readablebookstore@gmail.com', [to_email], fail_silently=False)

    return JsonResponse({
      'status': 'Your Payment is Successful',
      'order_id': order.order_id,
    })

  else:
    return HttpResponse('Failed')

def order_success(request):
    order_id = request.GET.get('order_id')
    try:
      order = Order.objects.get(order_id=order_id)
      context = {
        'order': order,
        'order_id':order_id
      }
      return render(request, 'orders/order-success.html', context)
    except Order.DoesNotExist:
      return redirect('home')
