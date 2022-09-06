from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name="admin-login"),  
	  path('logout/', views.admin_logout, name="admin-logout"),

    path('user-management/', views.user_management, name='user-management'),
    path('user-management/block/<str:pk>/', views.block_user , name='block-user'),
    path('user-management/unblock/<str:pk>/', views.unblock_user , name='unblock-user'),

    path('category-management/', views.category_management, name='category-management'),
    path('category-management/category/delete/<str:pk>/', views.del_category, name='del-category'),
    path('category-management/sub-category/delete/<str:pk>/', views.del_sub_category, name='del-sub-category'),
    path('category-management/language/delete/<str:pk>/', views.del_language, name='del-language'),

    path('product-management/', views.product_management, name='product-management'),
    path('product-management/add-product/', views.add_product, name='add-product'),
    path('product-management/product/delete/<str:pk>/', views.del_product, name='del-product'),
    path('product-management/product/edit/<str:pk>/', views.edit_product, name='edit-product'),



]