from django.contrib import admin
from .models import *
from products.models import Variation

class CartAdmin(admin.ModelAdmin):
  list_display = ('cart_id', 'date_created')

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('user','cart', 'product', 'quantity','is_active')

  # def formfield_for_manytomany(self, db_field, request, **kwargs):
  #     if db_field.name == "variation":
  #         product = Products.objects.get()
  #         kwargs["queryset"] = Variation.objects.filter(product=product.id)
  #     return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ShippingCharge)
