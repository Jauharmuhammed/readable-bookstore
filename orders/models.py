from django.db import models
from accounts.models import CustomUser, Address
from products.models import Products, Variation

# Create your models here.
class Payment(models.Model):

    status=(
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Failed','Failed'),
        ('Successful','Successful'),
        ('Refunded','Refunded'),
    )

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100, choices=status,default='Pending')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class ShippingMethod(models.Model):
    shipping_method = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=255)
    charge = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
      return self.shipping_method


status=(
    ('Pending','Pending'),
    ('Placed','Placed'),
    ('Processing','Processing'),
    ('Shipped','Shipped'),
    ('Out for Delivery','Out for Delivery'),
    ('Delivered','Delivered'),
    ('Returned','Returned'),
    ('Return Confirmed','Return Confirmed'),
    ('Cancelled','Cancelled'),
)

class Order(models.Model):
    

    user=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    payment=models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True, null=True)
    order_id=models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    gross_amount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    coupon_discount = models.PositiveIntegerField()
    shipping_charge = models.PositiveIntegerField()
    order_total=models.FloatField()
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING)
    status=models.CharField(max_length=20,choices=status,default='Pending')
    ip=models.CharField(max_length=20,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.order_id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20,choices=status)
    note = models.TextField(max_length = 500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.order_id)

class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation, blank=True)
    quantity=models.IntegerField()
    price = models.PositiveIntegerField()
    offer_price = models.PositiveIntegerField()
    gross_amount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def total_amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name



class Coupon(models.Model):
    coupon_code = models.CharField(max_length=25, unique=True)
    coupon_discount = models.PositiveIntegerField()
    coupon_description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
      return self.coupon_code


class CouponCheck(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


