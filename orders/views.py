from multiprocessing import context
from django.shortcuts import render, redirect
from accounts.models import Address
from products.models import Products, Variation

from carts.models import CartItem, ShippingCharge
from orders.models import Order, Payment, OrderProduct
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

def save_address(request, sub_total=0, total=0, shipping_charge = 0, quantity=0):
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
          if data.__eq__(existing_address):
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
      quantity += cart_item.quantity


    shipping_charge = ShippingCharge.objects.first()
    shipping_cost = 0
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    total = sub_total + shipping_cost


    context = {
      'cart_items' : cart_items,
      'addresses': addresses,
      'sub_total': sub_total,
      'shipping_charge': shipping_cost,
      'total' : total,
      'quantity' : quantity
    }
    return render(request, 'orders/select-address.html', context)

  else:
    return redirect('checkout')



def shipping_method(request, sub_total=0, total=0, shipping_charge = 0, quantity=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  if cart_items_count <= 0:
    return redirect('cart')

  if request.method == "POST":
    
    address_id = request.POST.get('address')

    for cart_item in cart_items:
      sub_total += cart_item.item_total()
      quantity += cart_item.quantity


    shipping_charge = ShippingCharge.objects.first()
    shipping_cost = 0
    if sub_total <= shipping_charge.range_upto:
      shipping_cost = shipping_charge.shipping_charge

    total = sub_total + shipping_cost

    address = Address.objects.get(user=current_user, id=int(address_id))


    context = {
      'cart_items' : cart_items,
      'address': address,
      'sub_total': sub_total,
      'shipping_charge': shipping_cost,
      'total' : total,
      'quantity' : quantity
    }
    return render(request, 'orders/shipping.html', context)


def payment_method(request, sub_total=0, total=0, shipping_charge = 0, quantity=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  if cart_items_count <= 0:
    return redirect('cart')

  if request.method == "POST":
    shipping_method = request.POST['shipping-method']
    address_id = request.POST['address']
    print(address_id, type(address_id))

    for cart_item in cart_items:
      sub_total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    if sub_total < 499:
      shipping_charge = 99

    if shipping_method == 'express':
      shipping_charge += 249

    total = sub_total + shipping_charge

    address = Address.objects.get(user=current_user, id=int(address_id))



    context = {
      'cart_items' : cart_items,
      'address': address,
      'shipping_method':shipping_method,
      'sub_total': sub_total,
      'shipping_charge': shipping_charge,
      'total' : total,
      'quantity' : quantity
    }

    return render(request, 'orders/payment-method.html', context)




def place_order(request, sub_total=0, total=0, shipping_charge = 0, quantity=0):
  current_user = request.user

  cart_items = CartItem.objects.filter(user=current_user)
  cart_items_count = cart_items.count()
  if cart_items_count <= 0:
    return redirect('cart')

  if request.method == "POST":
    shipping_method = request.POST['shipping-method']
    address_id = request.POST['address']

    payment_method = request.POST['payment-method']
    print(payment_method, type(payment_method))

    for cart_item in cart_items:
      sub_total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    if sub_total < 499:
      shipping_charge = 99

    if shipping_method == 'express':
      shipping_charge += 249

    total = sub_total + shipping_charge

    data = Order()

    ip_address = request.META.get('REMOTE_ADDR')
    address = Address.objects.get(user=current_user, id=int(address_id))

    data.user = current_user
    data.order_total = total
    data.address = address
    data.ip= ip_address
    data.shipping_method = shipping_method
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
        orderproduct.amount=item.product.price
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

      # return render(request, 'orders/order-success.html')
      return redirect('/orders/order-success/' +'?order_id='+order.order_id)

    elif payment_method == 'razorpay':
      order.is_ordered = True

      order.status = 'Pending'
      order.save()

      order_products=[]
      for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order = order
        orderproduct.user=request.user
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        orderproduct.amount=item.product.price
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

      order_products = OrderProduct.objects.filter(order = order.id)
      for order_product in order_products:
        if order_product is None:
          order = Order.objects.get(id= order_product.order.id)
          order.is_ordered = False
          order.save()



      context = {
        'order' : order,
        'payment_method' : payment_method,
        'shipping_method' : order.shipping_method,
        'order_products' : order_products,
        'sub_total': sub_total,
        'shipping_charge': shipping_charge,
        'total' : order.order_total,
        'quantity' : quantity
      }

      return render(request, 'orders/payment.html', context)


def razorpay_pay_now(request):
  order = Order.objects.filter(user=request.user).order_by('-created_date').first()
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
  order = Order.objects.filter(user=request.user).order_by('-created_date').first()
  if request.method == 'POST':
    payment_method = request.POST['payment_method']
    payment_id = request.POST.get('payment_id')
    amount = request.POST['payment_amount']

    payment= Payment()
    payment.payment_method = payment_method
    payment.user = request.user
    payment.amount = amount

    payment.payment_id= payment_id
    payment.status = 'Successful'

    payment.save()

    order.payment = payment
    order.status = 'Placed'
    order.save()

    order_products = CartItem.objects.filter(user=request.user)

    for orderproduct in order_products:
      orderproduct.payment=payment
      orderproduct.save()


    # Send order recieved email to to the customer
    mail_subject = 'Your order has been successfully placed'
    message = render_to_string('orders/order-received-email-prepaid.html',{
        'user' : request.user,
        'product': order_products,
        'amount': order.order_total,
        'payment_id':payment_id,
        'address': order.address,
        'order_id': order.order_id,
        'order_date':order.updated_date,
    })
    to_email = request.user.email
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
