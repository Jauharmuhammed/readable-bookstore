from django.contrib import admin

from .models import Coupon, CouponCheck, Order, OrderDetails, Payment, OrderProduct, ShippingMethod
class OrderProductInline(admin.TabularInline):
    model= OrderProduct
    list_display=['order','product','variation','price','quantity','gross_amount', 'discount', 'total']
    readonly_fields=('payment','user','product','quantity','total','order')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','user','order_total','status','is_ordered','created_date']
    list_filter=['status','is_ordered']
    search_fields=['order_id']
    list_per_page=20
    inlines=[OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','user','amount','status','payment_method','created_date']
    list_filter=['status']
    search_fields=['payment_id']
    list_per_page=20

class OrderProductAdmin(admin.ModelAdmin):
    list_display=['order','product','price','quantity','gross_amount', 'discount', 'total']
    list_per_page=20

class ShippingMethodAdmin(admin.ModelAdmin):
  list_display=['shipping_method','charge','is_active']

class OrderDetailsAdmin(admin.ModelAdmin):
  list_display=['order','order_status','date']

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Coupon)
admin.site.register(CouponCheck)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
