from django.urls import path
from . import views

urlpatterns = [
  path('address/save-address/', views.save_address , name='save-address'),
  path('shipping-method/', views.shipping_method , name='shipping-method'),
  path('payment-method/', views.payment_method , name='payment-method'),
  path('place-order/', views.place_order , name='place-order'),
  path('place-order/payment/', views.payment , name='payment'),
  path('order-success/', views.order_success , name='order-success'),

  path('coupon/apply-coupon/', views.applyCoupon, name='apply-coupon'),

  path('proceed-order/', views.razorpay_pay_now , name='proceed-order'),
]