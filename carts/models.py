from django.db import models
from products.models import Products

class Cart(models.Model):
  cart_id = models.CharField(max_length=255, blank=True)
  date_created = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.cart_id

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)
  modified_time = models.DateTimeField(auto_now=True)

  def sub_total(self):
    return self.product.price * self.quantity
    
  def __str__(self):
    return self.product