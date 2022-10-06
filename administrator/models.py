from django.db import models

# Create your models here.

class Banner(models.Model):
  banner_image = models.ImageField(upload_to='images/banner')
  title = models.CharField(max_length = 255)
  tagline = models.CharField(max_length = 255)
  updated_date = models.DateTimeField(auto_now=True)