from django.contrib import admin
from .models import Binding, Category, Language, SubCategory

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'slug')

class SubCategoryAdmin(admin.ModelAdmin):
  list_display = ('subcategory_name', 'slug', 'category')

class LanguageAdmin(admin.ModelAdmin):
  # prepopulated_fields = {'slug':('language_name',)}
  list_display = ('language_name', 'slug',)

class BindingAdmin(admin.ModelAdmin):
  list_display = ('binding_name', 'slug',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Binding, BindingAdmin)

