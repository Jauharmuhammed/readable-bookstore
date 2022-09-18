from django.contrib import admin
from .models import Products, Variation


class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'author', 'sub_category', 'stock', 'is_available')

class VariationAdmin(admin.ModelAdmin):
  list_display = ('product', 'variation_category', 'variation_value', 'is_available',)
  list_editable = ('is_available',)
  list_filter = ('product', 'variation_category', 'variation_value', 'is_available',)

admin.site.register(Products, ProductAdmin)
admin.site.register(Variation, VariationAdmin)