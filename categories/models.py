from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

class Category(models.Model):
  category_name = models.CharField(max_length=50, unique=True)
  slug = AutoSlugField(populate_from='category_name', max_length=100, unique=True,)
  description = models.TextField(max_length=255, blank=True)
  image = models.ImageField(upload_to='images/categories', blank=True)

  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'

  def get_url(self):
    return reverse('products-by-category', args=[self.slug])

  def __str__(self):
    return self.category_name


class SubCategory(models.Model):
  subcategory_name = models.CharField(max_length=50, unique=True)
  slug = AutoSlugField(populate_from='subcategory_name', max_length=100, unique=True,)
  category = models.ForeignKey('Category', on_delete=models.CASCADE) 
  description = models.TextField(max_length=255, blank=True)
  image = models.ImageField(upload_to='images/subcategories', blank=True)

  class Meta:
    verbose_name = 'sub category'
    verbose_name_plural = 'sub categories'

  def get_url(self):
    return reverse('products-by-sub-category', args=[self.category.slug, self.slug])

  def __str__(self):
    return self.subcategory_name


class Language(models.Model):
  language_name = models.CharField(max_length=50, unique=True)
  slug = AutoSlugField(populate_from='language_name', max_length=100, unique=True,)
  description = models.TextField(max_length=255, blank=True)
  image = models.ImageField(upload_to='images/subcategories', blank=True)

  class Meta:
    verbose_name = 'language'
    verbose_name_plural = 'languages'

  def get_url(self):
    return reverse('products-by-language', args=[self.slug])

  def __str__(self):
    return self.language_name

class Binding(models.Model):
  binding_name = models.CharField(max_length=50, unique=True)  
  slug = AutoSlugField(populate_from='binding_name', max_length=100, unique=True,)


  class Meta:
    verbose_name = 'bindings'
    verbose_name_plural = 'binding'

  def __str__(self):
    return self.binding_name