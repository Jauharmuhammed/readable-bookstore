from multiprocessing import context
from unicodedata import name
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from django.db.models import Q

from accounts.models import CustomUser, Subscriber
from administrator.forms import BannerForm
from categories.models import Category, SubCategory, Language
from categories.forms import CategoryCreationForm, SubCategoryCreationForm, LanguageCreationForm
from administrator.models import Banner
from orders.forms import CouponForm
from orders.models import Coupon, Order, OrderDetails, OrderProduct, Payment
from orders.views import payment

from products.models import Products, Variation
from products.forms import ProductCreationForm

from django.http import JsonResponse, HttpResponse

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from datetime import datetime, timedelta
import calendar
import json


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            user= authenticate(email =email, password = password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid login credentials")
        return render(request, 'administrator/admin-login.html')


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def dashboard(request):
    today = datetime.today().date()
    yesterday = today - timedelta(1)

    User = get_user_model()
    total_users_count = User.objects.all().count()
    active_users_count = User.objects.filter(is_active=True).count()
    non_active_users_count = total_users_count - active_users_count
    new_users_today = User.objects.filter(date_joined__date=today, is_active = True).count()

    total_subscribers_count = Subscriber.objects.all().count()
    new_subscribers_today = Subscriber.objects.filter(subscribed_date__date=today).count()

    total_orders_count = Order.objects.filter(is_ordered=True).count()
    new_orders_today = Order.objects.filter(created_date__date=today, is_ordered=True).count()

    placed_orders_count = Order.objects.filter(is_ordered=True, status='Placed').count() + Order.objects.filter(is_ordered=True, status='Processing').count()
    shipped_orders_count = Order.objects.filter(is_ordered=True, status='Shipped').count()
    out_for_delivery_orders_count = Order.objects.filter(is_ordered=True, status='Out for Delivery').count()
    delivered_orders_count = Order.objects.filter(is_ordered=True, status='Delivered').count()
    cancelled_orders_count = Order.objects.filter(is_ordered=True, status='Cancelled').count()
    returned_orders_count = Order.objects.filter(is_ordered=True, status='Returned').count() +  Order.objects.filter(is_ordered=True, status='Return Confirmed').count()

    all_orders = Order.objects.filter(is_ordered=True)
    total_order_amount = 0
    for order in all_orders:
      total_order_amount += order.order_total

    todays_orders = Order.objects.filter(is_ordered=True, created_date__date=today)
    total_order_amount_today = 0
    for todays_order in todays_orders:
      total_order_amount_today += todays_order.order_total

    total_products = Products.objects.all()
    total_products_count = total_products.count()
    total_products_stock = 0
    out_of_stock_items = 0
    low_stock_items = 0
    for products in total_products:
      total_products_stock += products.stock
      if products.stock == 0:
        out_of_stock_items += 1
      if products.stock < 10 :
        low_stock_items += 1

    total_languages = Language.objects.all().count() - 1
    total_categories = Category.objects.all().count() 
    total_subcategories = SubCategory.objects.all().count() 

    last_week_sale = []
    day = datetime.today().date()
    weekday_list = []
    for _ in range(10):
      day_orders = Order.objects.filter(is_ordered=True, created_date__date=day)
      sale_of_the_day = 0
      for order in day_orders:
        sale_of_the_day += order.order_total
      last_week_sale.append(round(sale_of_the_day))
      weekday_list.append(calendar.day_abbr[day.weekday()])
      day = day - timedelta(1)

    last_week_sale.reverse()
    weekday_list.reverse()
    last_week_sale_json = json.dumps(last_week_sale)
    weekday_list_json = json.dumps(weekday_list)


    successful_payment_orders = Order.objects.filter(is_ordered=True)
    razorpay_transactions = 0
    pay_on_delivery_transactions =0 
    pending_transactions = 0
    refunds = 0
    all_transactions = 0 
    for order in successful_payment_orders:
      if order.payment.payment_method == 'razorpay' and  order.payment.status == 'Successful':
        razorpay_transactions += order.order_total
      elif order.payment.payment_method == 'payOnDelivery' and  order.payment.status == 'Successful':
        pay_on_delivery_transactions += order.order_total

      if order.payment.status == 'Pending':
        pending_transactions += order.order_total

      if order.payment.status == 'Refunded':
        refunds += order.order_total

      if order.payment.status == 'Refunded' or order.payment.status == 'Successful':
        all_transactions += order.order_total

    all_successful_transactions = razorpay_transactions + pay_on_delivery_transactions


    order_products = OrderProduct.objects.filter(is_ordered=True)
    order_product_dict = {}
    for order_product in order_products:
      if order_product.product.name in order_product_dict:
        quantity = order_product_dict[order_product.product.name]
        quantity += order_product.quantity
        order_product_dict[order_product.product.name] = quantity
      else:
        order_product_dict[order_product.product.name]=order_product.quantity

    sorted_order_product_dict = dict(sorted(order_product_dict.items(), key=lambda item: item[1], reverse=True))

    sorted_products_by_sales = list(sorted_order_product_dict.keys())
    sorted_product_quantity_by_sales = list(sorted_order_product_dict.values())
    print(order_product_dict)
    print(sorted_order_product_dict)
    print(sorted_products_by_sales)
    print(sorted_product_quantity_by_sales)



    context = {
        'total_users_count' : total_users_count,
        'active_users_count': active_users_count,
        'non_active_users_count':non_active_users_count,
        'new_users_today':new_users_today,

        'subscribers_count':total_subscribers_count,
        'new_subscribers_today':new_subscribers_today,
        
        'total_orders_count':total_orders_count,
        'new_orders_today':new_orders_today,
        'placed_orders_count': placed_orders_count,
        'shipped_orders_count': shipped_orders_count,
        'out_for_delivery_orders_count': out_for_delivery_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'cancelled_orders_count': cancelled_orders_count,
        'returned_orders_count': returned_orders_count,

        'total_order_amount': round(total_order_amount),
        'total_order_amount_today':round(total_order_amount_today),

        'total_products_count': total_products_count,
        'total_products_stock':total_products_stock,
        'out_of_stock_items':out_of_stock_items,
        'low_stock_items':low_stock_items,

        'total_languages':total_languages,
        'total_categories':total_categories,
        'total_subcategories':total_subcategories,

        'last_week_sale':last_week_sale_json,
        'weekday_list':weekday_list_json,

        'all_successful_transactions':round(all_successful_transactions),
        'razorpay_transactions':round(razorpay_transactions),
        'pay_on_delivery_transactions': round(pay_on_delivery_transactions),
        'pending_transactions':round(pending_transactions),
        'refunds':round(refunds),
        'all_transactions': round(all_transactions),

        'sorted_products_by_sales':json.dumps(sorted_products_by_sales[:4]),
        'sorted_product_quantity_by_sales':json.dumps(sorted_product_quantity_by_sales[:4]),

    }
    return render(request, 'administrator/index.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def user_management(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')

    if users is not None:
      paginator = Paginator(users, 10)
      page = request.GET.get('page')
      paged_users = paginator.get_page(page)
    else:
      paged_users = None

    context = {
        'users' : paged_users,
    }
    return render(request, 'administrator/user-management.html', context)



  
@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def user_search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword :
      User = get_user_model()
      users = User.objects.filter(
        Q(first_name__icontains=keyword) | 
        Q(last_name__icontains=keyword) | 
        Q(email__icontains=keyword) |
        Q(mobile_number__iexact=keyword)
      ).order_by('-date_joined')

      user_count = users.count()

      paginator = Paginator(users, 10)
      page = request.GET.get('page')
      paged_users = paginator.get_page(page)
  
    else:
      paged_users = None
      user_count = 0

  context = {
      'users' : paged_users,
      'user_count': user_count,
  }
  return render(request, 'administrator/user-management.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def subscriber_management(request):
    subscribers = Subscriber.objects.all().order_by('-subscribed_date')

    if subscribers is not None:
      paginator = Paginator(subscribers, 20)
      page = request.GET.get('page')
      paged_subscribers = paginator.get_page(page)
    else:
      paged_subscribers = None

    context = {
        'subscribers' : paged_subscribers,
    }
    return render(request, 'administrator/subscriber-management.html', context)


  
@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def subscriber_search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword :
      subscribers = Subscriber.objects.filter(
        email__icontains=keyword
      ).order_by('-subscribed_date')
      subscriber_count = subscribers.count()

      paginator = Paginator(subscribers, 10)
      page = request.GET.get('page')
      paged_subscribers = paginator.get_page(page)
  
    else:
      paged_subscribers = None
      subscriber_count = 0

  context = {
      'subscribers' : paged_subscribers,
      'subscriber_count':subscriber_count,
  }
  return render(request, 'administrator/subscriber-management.html', context)


@login_required(login_url= 'admin-login')
@staff_member_required(login_url='login')
def remove_subscription(request, pk):
  try:
    subscriber = Subscriber.objects.get(pk=pk)
    subscriber.delete()
  except Subscriber.DoesNotExist:
    pass
  return redirect('subscriber-management')

  
@login_required(login_url= 'admin-login')
@staff_member_required(login_url='login')
def block_user(request, pk):
    user = CustomUser.objects.get(pk = pk)
    user.is_active = False
    user.save()
    return redirect('user-management')


@login_required(login_url= 'admin-login')
@staff_member_required(login_url='login')
def unblock_user(request, pk):
    user = CustomUser.objects.get(pk = pk)
    user.is_active = True
    user.save()
    return redirect('user-management')


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def category_management(request):
    categories = Category.objects.all().order_by('id')
    sub_categories = SubCategory.objects.all().order_by('id')
    languages = Language.objects.all().order_by('id')

    category_form = CategoryCreationForm()
    sub_category_form = SubCategoryCreationForm()
    language_form = LanguageCreationForm()

    if request.method == 'POST' and 'language_submit' in request.POST:
        language_form = LanguageCreationForm(request.POST, request.FILES)
        if language_form.is_valid():
            language_form.save()
            return redirect('category-management')

        else:
            language_form= LanguageCreationForm(request.POST, request.FILES)

    if request.method == 'POST' and 'sub_category_submit' in request.POST:
        sub_category_form = SubCategoryCreationForm(request.POST, request.FILES)
        if sub_category_form.is_valid():
            sub_category_form.save()
            return redirect('category-management')

        else:
            sub_category_form= SubCategoryCreationForm(request.POST, request.FILES)

    if request.method == 'POST' and 'category_submit' in request.POST:
        category_form = CategoryCreationForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return redirect('category-management')

        else:
            # messages.error(request, 'Sub-category with the same name exists.')
            category_form= CategoryCreationForm(request.POST, request.FILES)


    context = {
      'categories' : categories,
      'sub_categories' : sub_categories,
      'languages' : languages,
      'category_form' : category_form,
      'sub_category_form' : sub_category_form,
      'language_form' : language_form,
    }
    return render(request, 'administrator/category-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def edit_category(request, pk):
  category_edit = Category.objects.get(pk=pk)
  if request.method == 'POST':
    edit_form = CategoryCreationForm(request.POST, request.FILES, instance=category_edit)
    if edit_form.is_valid():
      edit_form.save()
  return redirect('category-management')


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def edit_subcategory(request, pk):
  subcategory_edit = SubCategory.objects.get(pk=pk)
  if request.method == 'POST':
    edit_form = SubCategoryCreationForm(request.POST, request.FILES, instance=subcategory_edit)
    if edit_form.is_valid():
      edit_form.save()

  return redirect('category-management')



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def del_category(request, pk):
    del_cat = Category.objects.filter(pk=pk)
    del_cat.delete()
    return redirect('category-management')


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def del_sub_category(request, pk):
    del_sub = SubCategory.objects.filter(pk=pk)
    del_sub.delete()
    return redirect('category-management')



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def del_language(request, pk):
    del_lang = Language.objects.filter(pk=pk)
    del_lang.delete()
    return redirect('category-management')



# product management
@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def product_management(request):
    products = Products.objects.all().order_by('-modified_date')

    if products is not None:
      paginator = Paginator(products, 10)
      page = request.GET.get('page')
      paged_products = paginator.get_page(page)
    else:
      paged_products = None

    variations = Variation.objects.all()
    context = {
      'products' : paged_products,
      'variations': variations,
    }
    return render(request, 'administrator/product-management.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def product_search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword :
      products = Products.objects.filter(
          Q(name__icontains=keyword) | 
          Q(author__icontains=keyword) |
          Q(sub_category__subcategory_name__icontains=keyword) |
          Q(sub_category__category__category_name__iexact=keyword) |
          Q(isbn__iexact=keyword) |
          Q(language__language_name__iexact=keyword)
        ).order_by('-modified_date')

      paginator = Paginator(products, 10)
      page = request.GET.get('page')
      paged_products = paginator.get_page(page)
  
      product_count = products.count()
      variations = Variation.objects.all()
    else:
      paged_products = None
      product_count = 0
      variations = None


  context = {
    'products' : paged_products ,
    'product_count': product_count,
    'variations':variations,
  }
  return render(request, 'administrator/product-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def add_product(request):
    form = ProductCreationForm()
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            name = form.cleaned_data['name']
            product = Products.objects.get(name=name)

            format_list = request.POST.getlist('format[]')
            for format in format_list:
              Variation.objects.create(
                product = product,
                variation_category = 'format',
                variation_value = format
              )

            return redirect('product-management')

        else:
            messages.error(request, 'A product with the same name already exists.')
            form= ProductCreationForm(request.POST, request.FILES)

    context = {
      'form':form
    }
    return render(request, 'administrator/add-product.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def del_product(request, pk):
    product_del = Products.objects.filter(pk=pk)
    product_del.delete()
    return redirect('product-management')


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def edit_product(request, pk):
    product_edit = Products.objects.get(pk=pk)
    product_name = product_edit.name
    edit_form = ProductCreationForm(instance=product_edit)
    if request.method == 'POST':
        edit_form = ProductCreationForm(request.POST, request.FILES, instance=product_edit)
        if edit_form.is_valid():
            edit_form.save()

            format_list = request.POST.getlist('format[]')

            existing_variations_list = []
            existing_variations = Variation.objects.filter(product=product_edit)
            for existing_variation in existing_variations:
              variation = existing_variation.variation_value
              existing_variations_list.append(variation)

            for format in format_list:
              if format not in existing_variations_list:
                Variation.objects.create(
                  product = product_edit,
                  variation_category = 'format',
                  variation_value = format
                )
            for existing_variation_item in existing_variations_list:
              if existing_variation_item not in format_list:
                variation = Variation.objects.get(product = product_edit, variation_value = existing_variation_item)
                print(variation)
                variation.delete()

            return redirect('product-management')
        else:
            messages.error(request, 'Invalid details')
            return redirect('edit-product',pk)
    
    context = {
      'form' : edit_form,
      'product_id':product_edit,
      'product_name': product_name,
    }
    return render(request, 'administrator/edit-product.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def order_management(request):
  orders = Order.objects.filter(is_ordered=True).order_by('-created_date')

  if orders is not None:
    paginator = Paginator(orders, 20)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
  else:
    paged_orders = None

  order_products = OrderProduct.objects.filter(is_ordered=True).order_by('-created_date')
  statuses = ['Pending', 'Placed','Processing','Shipped','Delivered','Returned','Return Confirmed','Cancelled',]
  context = {
    'order_products':order_products,
    'orders':paged_orders,
    'statuses':statuses,
  }
  return render(request, 'administrator/order-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def filtered_orders(request, order_status):
  orders = Order.objects.filter(is_ordered=True, status = order_status).order_by('-created_date')

  if orders is not None:
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
  else:
    paged_orders = None

  order_products = OrderProduct.objects.filter(is_ordered=True).order_by('-created_date')
  statuses = ['Pending', 'Placed','Processing','Shipped','Delivered', 'Out for Delivery','Returned','Return Confirmed','Cancelled',]
  context = {
    'order_products':order_products,
    'orders':paged_orders,
    'statuses':statuses,
  }
  return render(request, 'administrator/order-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def update_order_status(request, order_id):
  order_status = request.GET.get('order_status')
  print(order_status)
  if order_status is not None:
    order = Order.objects.get(id=order_id)
    order.status = order_status
    order.save()

    # create order date object for the order
    OrderDetails.objects.create(
      order = order,
      order_status = order.status,
    )

    if order_status == 'Cancelled':
      order_products = OrderProduct.objects.filter(order=order.id)
      for order_product in order_products:
        product = Products.objects.get(id=order_product.product_id)
        product.stock += order_product.quantity
        product.save()

      payment = Payment.objects.get(id=order.payment.id)
      if order.payment.payment_method == 'payOnDelivery':
        payment.status = 'Failed'
        payment.save()

      elif order.payment.payment_method == 'razorpay':
        payment.status = 'Refunded'
        payment.save()
        
    if order_status == 'Delivered' and order.payment.payment_method == 'payOnDelivery':

      payment = Payment.objects.get(id=order.payment.id)
      payment.status = 'Successful'
      payment.save()

    if order_status == 'Return Confirmed':

      payment = Payment.objects.get(id=order.payment.id)
      payment.status = 'Refunded'
      payment.save()

      # increase the inventory stock if the product is returned
      order_products = OrderProduct.objects.filter(order=order.id)
      for order_product in order_products:
        product = Products.objects.get(id=order_product.product_id)
        product.stock += order_product.quantity
        product.save()
        
    return JsonResponse({
      'status' : 'Order status updated successfully'
    })
  else:
    return HttpResponse()



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def payment_management(request):
  payments = Payment.objects.all().order_by('-created_date')

  if payments is not None:
    paginator = Paginator(payments, 10)
    page = request.GET.get('page')
    paged_payments = paginator.get_page(page)
  else:
    paged_payments = None

  orders = Order.objects.filter(is_ordered=True)
  context = {
    'payments':paged_payments,
    'orders':orders,
  }
  return render(request, 'administrator/payment-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def order_search(request):
  if 'keyword' in request.GET:
    keyword = request.GET.get('keyword')
    if keyword :

      orders = Order.objects.filter(
          Q(user__email__icontains=keyword) | 
          Q(user__first_name__icontains=keyword) | 
          Q(user__last_name__icontains=keyword) | 
          Q(status__icontains=keyword) | 
          Q(payment__status__icontains=keyword) | 
          Q(payment__payment_method__icontains=keyword) | 
          Q(payment__payment_id__iexact=keyword) |
          Q(shipping_method__shipping_method__iexact=keyword) |
          Q(order_id__iexact=keyword)
        ).order_by('-created_date')
      orders_count = orders.count()

      paginator = Paginator(orders, 10)
      page = request.GET.get('page')
      paged_orders = paginator.get_page(page)

      order_products = OrderProduct.objects.filter(is_ordered=True).order_by('-created_date')
      statuses = ['Pending', 'Placed','Processing','Shipped','Delivered','Returned','Return Confirmed','Cancelled',]
    else:
      paged_orders = None
      order_products = None
      statuses = None

  context = {
    'order_products':order_products,
    'orders':paged_orders,
    'statuses':statuses,
    'orders_count':orders_count,
  }
  return render(request, 'administrator/order-management.html', context)



@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def payment_search(request):
  if 'keyword' in request.GET:
    keyword = request.GET.get('keyword')
    if keyword :
      payments = Payment.objects.filter(
        Q(user__email__icontains=keyword) | 
        Q(status__icontains=keyword) | 
        Q(payment_method__icontains=keyword) | 
        Q(amount__iexact=keyword) | 
        Q(payment_id__iexact=keyword)
      ).order_by('-created_date')
      payment_count = payments.count

      paginator = Paginator(payments, 10)
      page = request.GET.get('page')
      paged_payments = paginator.get_page(page)

      orders = Order.objects.filter(is_ordered=True)

    else:
      paged_payments = None
      orders = None

  context = {
    'payments':paged_payments,
    'orders':orders,
    'payment_count':payment_count,
  }
  return render(request, 'administrator/payment-management.html', context)



def banner_management(request):
  banner = Banner.objects.first()
  form = BannerForm()
  if request.method == 'POST':
    banner_id = request.POST['banner_id']
    update_banner = Banner.objects.get(id=banner_id)
    form = BannerForm(request.POST, request.FILES, instance=update_banner)
    if form.is_valid():
      form.save()
    else:
      print(form.errors)
  context = {
    'banner' : banner,
    'form': form,
  }
  return render(request, 'administrator/banner-management.html', context)


def coupon_management(request):
  coupons = Coupon.objects.all()
  context = {
    'coupons':coupons,
  }
  return render(request, 'administrator/coupon-management.html', context)
  

def add_coupon(request):
  if request.method == 'POST':
    form = Coupon()
    form.coupon_code = request.POST['coupon_code']
    form.coupon_discount = request.POST['coupon_discount']
    form.coupon_description = request.POST['coupon_description']
    if request.POST.get('is_active') == 'on':
      form.is_active = True
    else:
      form.is_active = False

    form.save()

    return redirect('coupon-management')

def delete_coupon(request, pk):
  try:
    del_coupon = Coupon.objects.get(pk=pk)
  except Coupon.ObjectDoesNotExist:
    messages.error(request, 'Sorry an error occured')
  
  if del_coupon is not None:
    del_coupon.delete()
    messages.success(request, 'Coupon deleted successfully')

  return redirect('coupon-management')

def edit_coupon(request, pk):
  if request.method == 'POST':
    try:
      edit_coupon = Coupon.objects.get(pk=pk)
    except Coupon.ObjectDoesNotExist:
      messages.error(request, 'Sorry an error occured')

    if edit_coupon:
      edit_form = CouponForm(request.POST, instance=edit_coupon)
      if edit_form.is_valid():
        edit_form.save()
      messages.success(request, 'Changes saved successfully')

  return redirect('coupon-management')
