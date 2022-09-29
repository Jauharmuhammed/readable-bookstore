from email.policy import default
from django.db import models
from django.db.models import Avg, Count
from accounts.models import CustomUser
from categories.models import Category, SubCategory, Language

from autoslug import AutoSlugField

from django.urls import reverse



class Products(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = AutoSlugField(populate_from='name', max_length=100, unique=True)
  isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
  sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
  language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

  author = models.CharField(max_length=100)
  Publisher = models.CharField(max_length=100, blank=True, default=None)
  release_date = models.DateField(blank=True, null=True, default=None)

  price = models.PositiveIntegerField(default=None)
  discount = models.PositiveBigIntegerField(blank=True, default=0)

  stock = models.PositiveIntegerField(default=None)
  is_available = models.BooleanField(default=True)

  cover_image = models.ImageField(upload_to='images/products')
  image1 = models.ImageField(upload_to='images/products', blank=True, default=None, null=True)
  image2 = models.ImageField(upload_to='images/products', blank=True, default=None, null=True)
  image3 = models.ImageField(upload_to='images/products', blank=True, default=None, null=True)

  description = models.TextField(max_length=2000, blank=True, default=None)
  create_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  number_of_pages = models.IntegerField(blank=True, null=True)
  weight = models.IntegerField(blank=True, null=True)
  width = models.IntegerField(blank=True, null=True)
  height = models.IntegerField(blank=True, null=True)
  spine_width = models.IntegerField(blank=True, null=True)


  class Meta:
    verbose_name = 'Product'
    verbose_name_plural = 'Products'

  def get_url(self):
    return reverse('product-view', args=[self.slug])

  def average_review(self):
    reviews=Review.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
    avg=0
    if reviews['average'] is not None:
        avg=float(reviews['average'])
    return avg


  def review_count(self):
    reviews=Review.objects.filter(product=self,status=True).aggregate(count=Count('id'))
    count=0
    if reviews['count'] is not None:
        count=int(reviews['count'])
    return count

  def offer_price(self):
    category_offer_discount = self.price * self.sub_category.discount / 100
    price = self.price - category_offer_discount
    product_discount = self.price * self.discount / 100
    price = price - product_discount
    if price > 0 and price < self.price :
      return round(price)
    else:
      return self.price

  def offer(self):
    offer = self.discount + self.sub_category.discount 
    if offer > 0 and offer <100:
      return offer
    else: 
      return None

  def __str__(self):
    return self.name





class Variation(models.Model):

  variation_category_choice = (
    ('format', 'format'),
  )
  variation_value_choice = (
    ('paperback', 'Paperback'),
    ('hardcover','Hard Cover'),
    ('ebook','Ebook'),
    ('audiobook','Audiobook'),
  )

  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  variation_category = models.CharField(max_length=100, choices=variation_category_choice)
  variation_value = models.CharField(max_length=100, choices=variation_value_choice)
  is_available = models.BooleanField(default=True)  
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.variation_value



class Review(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=1000,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
