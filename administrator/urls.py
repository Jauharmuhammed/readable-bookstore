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

    path('order-management/', views.order_management, name='order-management'),
    path('order-management/placed-orders/', views.placed_orders, name='placed-orders'),
    path('order-management/pending-orders/', views.pending_orders, name='pending-orders'),
    path('order-management/cancelled-orders/', views.cancelled_orders, name='cancelled-orders'),
    path('order-management/completed-orders/', views.completed_orders, name='completed-orders'),
    path('order-management/closed-orders/', views.closed_orders, name='closed-orders'),

    # path('order-management/update-order-product-status/<int:order_product_id>/', views.update_order_product_status, name='update-order-product-status'),
    path('order-management/update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('payment-management/', views.payment_management, name='payment-management'),



]