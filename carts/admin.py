from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
  list_display = ('cart_id', 'date_created')

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('user','cart', 'product', 'quantity','is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
