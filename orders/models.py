from pyexpat import model
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


class Order(models.Model):
    status=(
        ('Pending','Pending'),
        ('Placed','Placed'),
        ('Failed','Failed'),
        ('Processing','Processing'),
        ('Completed','Completed'),
        ('Closed','Closed'),
        ('Cancelled','Cancelled'),
    )

    shipping_method = (
        ('standard', 'Standard'),
        ('express', 'Express'),
    )

    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_id=models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    order_total=models.FloatField()
    shipping_method = models.CharField(max_length=20, choices=shipping_method, default='Standard')
    status=models.CharField(max_length=10,choices=status,default='Pending')
    ip=models.CharField(max_length=20,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.order_id)


class OrderProduct(models.Model):
    status =(
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Returned','Returned'),
        ('Return Confirmed','Return Confirmed'),
        ('Cancelled','Cancelled'),
    )
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation, blank=True)
    quantity=models.IntegerField()
    amount=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    status=models.CharField(max_length=20,choices=status,default='Processing')
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def total_amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
