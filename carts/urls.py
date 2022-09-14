from django.urls import path 
from django.shortcuts import render, redirect

from config import views

from . import views

urlpatterns = [
  path('', views.cart, name='cart'),
  path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
  path('remove_from_cart/<int:product_id>/<int:cart_item_id>/', views.remove_from_cart, name='remove-from-cart'),
  path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart-item'),

  path('checkout/', views.checkout, name='checkout'),
]