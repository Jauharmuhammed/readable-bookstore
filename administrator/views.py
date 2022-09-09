from itertools import product
from tkinter.messagebox import RETRY
from unicodedata import category, name
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from accounts.models import CustomUser
from categories.models import Category, SubCategory, Language, Binding
from categories.forms import CategoryCreationForm, SubCategoryCreationForm, LanguageCreationForm

from products.models import Products
from products.forms import ProductCreationForm


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
        return render(request, 'admin/admin-login.html')


@login_required(login_url='admin-login')
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
    return render(request, 'admin/index.html', context)


@login_required(login_url='admin-login')
@staff_member_required(login_url='login')
def user_management(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users' : users,
    }
    return render(request, 'admin/user-management.html', context)

  
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
    bindings = Binding.objects.all().order_by('id')

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
      'bindings' : bindings,
      'category_form' : category_form,
      'sub_category_form' : sub_category_form,
      'language_form' : language_form,
    }
    return render(request, 'admin/category-management.html', context)


def del_category(request, pk):
    del_cat = Category.objects.filter(pk=pk)
    del_cat.delete()
    return redirect('category-management')

def del_sub_category(request, pk):
    del_sub = SubCategory.objects.filter(pk=pk)
    del_sub.delete()
    return redirect('category-management')

def del_language(request, pk):
    del_lang = Language.objects.filter(pk=pk)
    del_lang.delete()
    return redirect('category-management')



# product management

def product_management(request):
    products = Products.objects.all().order_by('-modified_date')
    context = {
      'products' : products
    }
    return render(request, 'admin/product-management.html', context)

def add_product(request):
    form = ProductCreationForm()
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-management')

        else:
            messages.error(request, 'A product with the same name already exists.')
            form= ProductCreationForm(request.POST, request.FILES)

    context = {
      'form':form
    }
    return render(request, 'admin/add-product.html', context)

def del_product(request, pk):
    product_del = Products.objects.filter(pk=pk)
    product_del.delete()
    return redirect('product-management')

def edit_product(request, pk):
    product_edit = Products.objects.get(pk=pk)
    product_name = product_edit.name
    edit_form = ProductCreationForm(instance=product_edit)
    if request.method == 'POST':
        edit_form = ProductCreationForm(request.POST, request.FILES, instance=product_edit)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('product-management')
        else:
            messages.error(request, 'Invalid details')
            return redirect('edit-product',pk)
    
    context = {
      'form' : edit_form,
      'product_id':product_edit,
      'product_name': product_name,
    }
    return render(request, 'admin/edit-product.html', context)