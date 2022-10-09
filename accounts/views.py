import os
import re
from decouple import config

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail

from django.db.models import Count, ProtectedError
from django.http import HttpResponse, JsonResponse

from django.shortcuts import redirect, render, get_object_or_404

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderDetails, OrderProduct, Payment
from products.models import Products, Wishlist

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import *
from .forms import *

import requests

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                mobile_number = form.cleaned_data['mobile_number']

                username = email.split('@')[0]
                
                user = CustomUser.objects.create_user(first_name=first_name, email=email, password=password, username=username)

                user.mobile_number = mobile_number
                user.last_name = last_name

                user.save()

                UserProfile.objects.create(user=user)

                subscriber = Subscriber.objects.filter(email=email).exists()
                if not subscriber:
                  Subscriber.objects.create(email=email)

                #user activation using email id
                current_site = get_current_site(request)
                mail_subject = 'Activation email for your account'
                message = render_to_string('accounts/account_verification_email.html',{
                    'user' : user,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                })
                to_email = email
                send_mail(mail_subject, message, 'readablebookstore@gmail.com', [to_email], fail_silently=False)

                return redirect('/account/login/?command=verification&email='+email)
        
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def subscribe(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
      email = request.POST['email']
      if not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        messages.error(request, 'Invalid Email Address')
      elif Subscriber.objects.filter(email=email):
        messages.error(request, "Already subscribed to our Newsletter")
      else:
        Subscriber.objects.create(email=email)
        messages.success(request, "Subscription Successful")

        current_site = get_current_site(request)
        subscriber = Subscriber.objects.get(email=email)
        mail_subject = 'Subscription Successful'
        message = render_to_string('accounts/subscription-successful-email.html',{
            'subscriber' : subscriber,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(subscriber.pk)),
        })
        to_email = email
        send_mail(mail_subject, message, 'readablebookstore@gmail.com', [to_email], fail_silently=False)
    return redirect(url)

def unsubscribe(request, uidb64):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    subscriber = Subscriber.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
    subscriber = None

  if subscriber is not None:
    subscriber.delete()
    return HttpResponse('Unsubscribed Successfully')
  else:
    return HttpResponse('Sorry, an error occured')



@never_cache
def user_login(request):
    if request.user.is_authenticated :
        return redirect('home')
    else:

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            user= authenticate(email =email, password = password)

            if user is not None:
              try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                  cart_item=CartItem.objects.filter(cart=cart)

                  product_variations= []
                  product_id = []
                  for item in cart_item:
                    variation=item.variation.all()
                    product_variations.append(list(variation))
                    product_id.append(item.id)


                  cart_item=CartItem.objects.filter(user=user)
                  existing_variation_list=[]
                  id=[]
                  for item in cart_item:
                    existing_variation=item.variation.all()
                    existing_variation_list.append(list(existing_variation))
                    id.append(item.id)


                  for product_variation in product_variations:
                    if product_variation in existing_variation_list:
                      index=existing_variation_list.index( product_variation)
                      item_id=id[index]
                      item=CartItem.objects.get(id=item_id)
                      item.quantity += 1
                      item.user = user
                      item.save()

                    else:
                      index=product_variations.index( product_variation)
                      item_id=product_id[index]
                      item=CartItem.objects.get(id=item_id)
                      item.user = user
                      item.save()

              except:
                pass

              login(request, user)
              url = request.META.get('HTTP_REFERER')
              try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                  next_page = params['next']
                  return redirect(next_page)
              except:
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials")
        return render(request, 'accounts/login.html')


@never_cache
@login_required(login_url= 'login')
def user_logout(request):
    logout(request)
    return redirect('login')


def user_activate(request, uidb64, token):
    try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
      user = None

    if user is not None and default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      messages.success(request, 'Your account is activated successfully')
      return redirect('login')

    else:
      messages.error(request, 'Activation failed')
      return redirect('register')
    


@never_cache
def login_with_otp(request):
  if request.user.is_authenticated :
        return redirect('home')
  else:
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
          try:
            request.session['mobile_number'] = mobile_number

            account_sid = config('TWILIO_ACCOUNT_SID')
            auth_token = config('TWILIO_AUTH_TOKEN')
            client = Client(account_sid,auth_token)

            verification = client.verify \
                .services('VA9c891ebf0f6f2f35cd621eda6e927657') \
                .verifications \
                .create(to='+91'+mobile_number, channel='sms')

            print(verification.status)
            messages.success(request, 'OTP is send to +91 '+mobile_number)
            return redirect('login-with-otp-verify')
          except TwilioRestException:
            messages.error(request, 'An error occured')
            return redirect('login-with-otp')
        else:
            messages.error(request, 'Phone Number is not Registered')
            return redirect('login-with-otp')
    else:
        return render(request,'accounts/login-with-otp.html' )



@never_cache
def login_with_otp_verify(request):
  if request.user.is_authenticated :
        return redirect('home')
  else:
      if request.method == 'POST':
          otp = request.POST['otp']

          mobile_number= request.session['mobile_number']

          account_sid = config('TWILIO_ACCOUNT_SID')
          auth_token = config('TWILIO_AUTH_TOKEN')
          client = Client(account_sid, auth_token)

          verification_check = client.verify \
              .services('VA9c891ebf0f6f2f35cd621eda6e927657')\
              .verification_checks \
              .create(to='+91'+mobile_number, code=otp)

          print(verification_check.status)

          if verification_check.status == 'approved':

              user = CustomUser.objects.get(mobile_number=mobile_number)

              if user is not None:
                  login(request, user)
                  return redirect('home')
                  
              else:
                  return redirect('login-with-otp-verify')
          else:
              messages.error(request, 'OTP is incorrect')
              return redirect('login-with-otp-verify')
      else:
          return render(request,'accounts/login-with-otp-verify.html' )


@never_cache
def forgot_password(request):
  if request.method == 'POST':
    email = request.POST['email']
    if CustomUser.objects.filter(email__iexact = email).exists():
      user = CustomUser.objects.get(email=email)
      current_site = get_current_site(request)
      mail_subject = 'Password change request'
      message = render_to_string('accounts/forgot-password-email.html',{
          'user' : user,
          'domain' : current_site,
          'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
          'token' : default_token_generator.make_token(user),
      })
      to_email = email
      send_mail(mail_subject, message, 'readablebookstore@gmail.com', [to_email], fail_silently=False)

      messages.success(request, 'Password change email has been send to your email.')
      return redirect('login')

    else:
      messages.error(request, 'No account is registered with email id you entered!')
      return redirect('forgot-password')

  return render(request, 'accounts/forgot-password.html')


@never_cache
def forgot_password_verify(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = CustomUser._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    user = None

  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    return redirect('reset-password')
  else:
    messages.error(request, 'The link has been expired!')
    return redirect('login')

  
def reset_password(request):
  if request.method == 'POST':
    password = request.POST['new-password']
    confirm_password = request.POST['confirm-password']

    if password == confirm_password:
      uid = request.session.get('uid')
      user = CustomUser.objects.get(pk=uid)
      user.set_password(password)
      user.save()
      messages.success(request, 'Password changed successfully.')
      print('Password changed successfully')
      return redirect('login')
    else:
      messages.error(request, 'Password do not match!')
      return redirect('reset-password')
  return render(request, 'accounts/reset-password.html')



def wishlist(request):
  try:
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-created_date')
    wishlist_count = wishlist_items.count()

    paginator = Paginator(wishlist_items, 8)
    page = request.GET.get('page')
    paged_wishlist_items = paginator.get_page(page)

  except:
    paged_wishlist_items = None
    wishlist_count= 0
  context = {
    'wishlist_items': paged_wishlist_items,
    'wishlist_count': wishlist_count
  }

  return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
  in_wishlist = Wishlist.objects.filter(user=request.user, product_id= product_id).exists()
  if in_wishlist:
    messages.warning(request, 'Item is already in wishlist')
    return JsonResponse({ 'message': 'Item is already in wishlist'})
  else:
    Wishlist.objects.create(
      user = request.user,
      product_id = product_id
    )
    messages.success(request, 'Item added to your wishlist')
    return JsonResponse({ 'message': 'Item added to your wishlist'})



@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
  in_wishlist = Wishlist.objects.filter(user=request.user, product_id= product_id).exists()
  if in_wishlist:
    wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist')
  else:
    return redirect('wishlist')


@login_required(login_url='login')
def dashboard(request):
  orders_count = Order.objects.filter(user=request.user, is_ordered=True).count()
  addresses_count = Address.objects.filter(user= request.user, is_active=True).count()
  wishlist_count = Wishlist.objects.filter(user= request.user).count()
  cart_item_count = CartItem.objects.filter(user= request.user).count()
  context = { 
    'orders_count':orders_count,
    'addresses_count':addresses_count,
    'wishlist_items_count':wishlist_count,
    'cart_items_count':cart_item_count,
  }
  return render(request, 'accounts/dashboard.html', context)
  

@login_required(login_url='login')
def user_profile(request):
  user_profile =get_object_or_404(UserProfile, user=request.user)
  change_password_form = ChangePasswordForm(user= request.user)
  context = {
    'user_profile' : user_profile,
    'change_password_form':change_password_form
  }
  return render(request, 'accounts/profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
  user_profile =get_object_or_404(UserProfile, user=request.user)
  if request.method == 'POST':
    print('post')
    user_form = UserForm(request.POST, instance=request.user)
    user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
    if user_form.is_valid():
      print('user_valid')
      if user_profile_form.is_valid():
        print('profile_valid')
        user = UserForm()
        user.first_name = user_form.cleaned_data['first_name']
        user.last_name = user_form.cleaned_data['last_name']
        user.mobile_number = user_form.cleaned_data['mobile_number']
        profile = UserProfileForm()
        profile.date_of_birth = user_profile_form.cleaned_data['date_of_birth']
        profile.location = user_profile_form.cleaned_data['location']
        profile.profile_picture = user_profile_form.cleaned_data['profile_picture']
        user_form.save()
        user_profile_form.save()
        messages.success(request, 'Your Profile is updated successfuly')

  return redirect('user-profile')


@login_required(login_url='login')
def change_password(request):
  if request.method == 'POST':
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    check_current_password = request.user.check_password(current_password)
    print(check_current_password)
    if check_current_password:
      if new_password != confirm_password:
        messages.error(request, 'Passwords do not match!')
      else:
        try:
          validate_password(new_password)
          request.user.set_password(new_password)
          request.user.save()
          messages.success(request, 'Password changed successfully')
          print('Password changed successfully')
          return redirect('user-profile')

        except ValidationError as e:
          messages.error(request, str(e))
          print(str(e))
          return redirect('user-profile')
    else:
      messages.error(request, 'Make sure you entered old password correctly!')


  return redirect('user-profile')



@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_date')
  order_products = OrderProduct.objects.filter(user=request.user, is_ordered=True).order_by('-created_date')
  order_details = OrderDetails.objects.filter(order__in=orders)

  if orders is not None:
    paginator = Paginator(orders, 8)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
  else:
    paged_orders = None

  context = {
    'order_products':order_products,
    'orders':paged_orders,
    'order_details':order_details,
  }
  return render(request, 'accounts/orders.html', context)

@login_required(login_url='login')
def order_details(request, order_id):
  order = None
  order_products =None
  try:
    order = get_object_or_404(Order, user=request.user,order_id=order_id, is_ordered=True)
    order_products = OrderProduct.objects.filter(user=request.user, order_id=order, is_ordered=True)
    order_details = OrderDetails.objects.filter(order=order)
  except (Order.DoesNotExist or OrderProduct.DoesNotExist):
    order = None
    order_products =None
  context = {
    'order_products':order_products,
    'order':order,
    'order_details':order_details,
  }
  return render(request, 'accounts/order-details.html', context)

@login_required(login_url='login')
def cancel_order(request, id):
  url = request.META.get('HTTP_REFERER')
  if request.method == "POST":
    order_note = request.POST['order_note']
    order_cancel = Order.objects.get(id=id)
    if order_cancel.status == 'Pending' or order_cancel.status == 'Placed' or order_cancel.status == 'Shipped':

      order_products = OrderProduct.objects.filter(order=order_cancel.id)
      for order_product in order_products:
        product = Products.objects.get(id=order_product.product_id)
        product.stock += order_product.quantity
        product.save()

      if order_cancel.status == 'Placed' or order_cancel.status == 'Shipped':
        payment = Payment.objects.get(id=order_cancel.payment.id)
        if payment.payment_method == 'razorpay':
          payment.status = 'Refunded'
          payment.save()

        elif payment.payment_method == 'payOnDelivery':
          payment.status = 'Failed'
          payment.save()

      elif order_cancel.status == 'Pending':
        payment = Payment.objects.get(id=order_cancel.payment.id)
        payment.status = 'Failed'
        payment.save()

      order_cancel.status = 'Cancelled'
      order_cancel.save()

      # create order date object for the order
      OrderDetails.objects.create(
        order = order_cancel,
        order_status = order_cancel.status,
        note = order_note,
      )

      

      messages.success(request, 'Order cancelled successfully')

    elif order_cancel.status == 'Out for Delivery':
      messages.error(request, "We cannot process cancellation request once the item is out for delivery, Please contact with the our courier partner or help center. If you dont want the product, Please don't recieve the product!")

  return redirect(url)

@login_required(login_url='login')
def return_order(request, id):
  url = request.META.get('HTTP_REFERER')
  if request.method == "POST":
    order_note = request.POST['order_note']
    order_cancel = Order.objects.get(id=id)
    if order_cancel.status == 'Delivered':


      order_cancel.status = 'Returned'
      order_cancel.save()

      # create order date object for the order
      OrderDetails.objects.create(
        order = order_cancel,
        order_status = order_cancel.status,
        note = order_note,
      )

      messages.success(request, 'Return request recived')

  return redirect(url)


@login_required(login_url='login')
def address(request):
  addresses = Address.objects.filter(user= request.user, is_active=True).order_by('-date_added')
  context = {
    'addresses':addresses,
  }
  return render(request, 'accounts/address.html', context)

@login_required(login_url='login')
def add_new_address(request):
  current_user = request.user
  if request.method == 'POST':
    form = AddressForm(request.POST)
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

      data.save()
      messages.success(request, 'New address is saved successfully')

  return redirect('user-address')

@login_required(login_url='login')
def delete_address(request, address_id):
  try:
    del_address = Address.objects.get(id = address_id)
    del_address.delete()
  except ProtectedError:
    del_address.is_active = False
    del_address.save()
  return redirect('user-address')

@login_required(login_url='login')
def edit_address(request, address_id):
  try:
    edit_address = Address.objects.get(id = address_id)
    if request.method == 'POST':
      edit_form = AddressForm(request.POST, instance= edit_address)
      if edit_form.is_valid():
        edit_form.save()
      else:
        messages.error(request, 'Invalid details')
  except:
    pass
  return redirect('user-address')