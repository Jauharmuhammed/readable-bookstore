from unicodedata import category
from django.contrib import admin
from .models import Products
from categories.models import SubCategory


class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'author', 'sub_category', 'stock', 'is_available')


admin.site.register(Products, ProductAdmin)