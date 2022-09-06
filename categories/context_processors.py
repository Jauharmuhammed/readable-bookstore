from .models import Category, SubCategory, Language

def category_links(request):
  links = Category.objects.all()
  return dict(category_links=links)

def sub_category_links(request):
  links = SubCategory.objects.all()
  return dict(sub_category_links= links)

def language_links(request):
  links = Language.objects.all()
  return dict(language_links= links)