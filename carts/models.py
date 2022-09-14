from django.db import models
from products.models import Products, Variation

from accounts.models import CustomUser

class Cart(models.Model):
  cart_id = models.CharField(max_length=255, blank=True)
  date_created = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.cart_id

class CartItem(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  variation = models.ManyToManyField(Variation, blank=True)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)

  def item_total(self):
    return self.product.price * self.quantity
    
  def __str__(self):
    return self.product.name