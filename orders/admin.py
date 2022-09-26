from django.contrib import admin

from .models import Order, Payment, OrderProduct
class OrderProductInline(admin.TabularInline):
    model= OrderProduct
    readonly_fields=('payment','user','product','quantity','amount','order')
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
    list_display=['user','amount','status','created_date']
    list_filter=['status']
    list_per_page=20

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)