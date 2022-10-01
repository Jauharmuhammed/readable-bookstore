from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from django.db.models import Q

from accounts.models import CustomUser
from categories.models import Category, SubCategory, Language
from categories.forms import CategoryCreationForm, SubCategoryCreationForm, LanguageCreationForm
from orders.models import Order, OrderDetails, OrderProduct, Payment
from orders.views import payment

from products.models import Products, Variation
from products.forms import ProductCreationForm

from django.http import JsonResponse, HttpResponse

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



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
    User = get_user_model()
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'administrator/index.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def user_management(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users' : paged_users,
    }
    return render(request, 'administrator/user-management.html', context)

  
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
            # messages.error(request, 'Language with the same name exists.')
            language_form= LanguageCreationForm(request.POST, request.FILES)

    if request.method == 'POST' and 'sub_category_submit' in request.POST:
        sub_category_form = SubCategoryCreationForm(request.POST, request.FILES)
        if sub_category_form.is_valid():
            sub_category_form.save()
            return redirect('category-management')

        else:
            # messages.error(request, 'Sub-category with the same name exists.')
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

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)


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
      product_count = products.count()

      variations = Variation.objects.all()
    else:
      products = None
      product_count = 0
      variations = None

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
  
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
    print(product_edit, type(product_edit))
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

  paginator = Paginator(orders, 10)
  page = request.GET.get('page')
  paged_orders = paginator.get_page(page)

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

  paginator = Paginator(orders, 10)
  page = request.GET.get('page')
  paged_orders = paginator.get_page(page)

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

  paginator = Paginator(payments, 10)
  page = request.GET.get('page')
  paged_payments = paginator.get_page(page)

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
      orders = None
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
      payments = None
      orders = None
  context = {
    'payments':paged_payments,
    'orders':orders,
    'payment_count':payment_count,
  }
  return render(request, 'administrator/payment-management.html', context)
