from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name="products"),
    path('category/<slug:category_slug>/', views.products, name='products-by-category'),
    path('category/<slug:category_slug>/<slug:sub_category_slug>/', views.products, name='products-by-sub-category'),
    path('language/<slug:language_slug>/', views.products_by_language, name='products-by-language'),

    path('view/<slug:product_slug>/', views.product_view, name='product-view'),

    path('review/<int:product_id>/',views.review,name='review'),
    path('review/delete-review/<int:product_id>/',views.delete_review,name='delete-review'),

    path('search/', views.search, name='search'),
]