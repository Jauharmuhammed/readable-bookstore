import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail

from django.db.models import Count
from django.http import HttpResponse

from django.shortcuts import redirect, render

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from carts.models import Cart, CartItem
from carts.views import _cart_id

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
    


def login_with_otp(request):
  if request.user.is_authenticated :
        return redirect('home')
  else:
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
          try:
            request.session['mobile_number'] = mobile_number

            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
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



def login_with_otp_verify(request):
  if request.user.is_authenticated :
        return redirect('home')
  else:
      if request.method == 'POST':
          otp = request.POST['otp']

          mobile_number= request.session['mobile_number']

          account_sid = os.environ['TWILIO_ACCOUNT_SID']
          auth_token = os.environ['TWILIO_AUTH_TOKEN']
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

      messages.success(request, 'Password change email has been send successfully.')
      return redirect('login')

    else:
      messages.error(request, 'No account is registered with email id you entered!')
      return redirect('forgot-password')

  return render(request, 'accounts/forgot-password.html')


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
      return redirect('login')
    else:
      messages.error(request, 'Password do not match!')
      return redirect('reset-password')
  return render(request, 'accounts/reset-password.html')



