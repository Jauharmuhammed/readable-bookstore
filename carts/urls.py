from django.urls import path 
from django.shortcuts import render, redirect

from config import views

from . import views

urlpatterns = [
  path('', views.cart, name='cart'),
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
  path('remove-from-cart/<int:product_id>/<int:cart_item_id>/', views.remove_from_cart, name='remove-from-cart'),
  path('remove-cart-item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart-item'),
  path('move-to-wishlist/<int:product_id>/<int:cart_item_id>/', views.move_to_wishlist, name='move-to-wishlist'),

  path('checkout/', views.checkout, name='checkout'),
]