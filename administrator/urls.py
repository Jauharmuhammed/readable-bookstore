from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name="admin-login"),  
	  path('logout/', views.admin_logout, name="admin-logout"),

    path('user-management/', views.user_management, name='user-management'),
    path('user-management/search/', views.user_search, name='user-search'),
    path('user-management/block/<str:pk>/', views.block_user , name='block-user'),
    path('user-management/unblock/<str:pk>/', views.unblock_user , name='unblock-user'),

    path('subscriber-management/', views.subscriber_management, name='subscriber-management'),
    path('subscriber-management/search/', views.subscriber_search, name='subscriber-search'),
    path('subscriber-management/remove/<str:pk>/', views.remove_subscription, name='remove-subscription'),

    path('category-management/', views.category_management, name='category-management'),
    path('category-management/category/edit/<str:pk>/', views.edit_category, name='edit-category'),
    path('category-management/subcategory/edit/<str:pk>/', views.edit_subcategory, name='edit-subcategory'),
    path('category-management/category/delete/<str:pk>/', views.del_category, name='del-category'),
    path('category-management/sub-category/delete/<str:pk>/', views.del_sub_category, name='del-sub-category'),
    path('category-management/language/delete/<str:pk>/', views.del_language, name='del-language'),

    path('product-management/', views.product_management, name='product-management'),
    path('product-management/search/', views.product_search, name='product-search'),
    path('product-management/add-product/', views.add_product, name='add-product'),
    path('product-management/product/delete/<str:pk>/', views.del_product, name='del-product'),
    path('product-management/product/edit/<str:pk>/', views.edit_product, name='edit-product'),

    path('order-management/', views.order_management, name='order-management'),
    path('order-management/search/', views.order_search, name='order-search'),
    path('order-management/<str:order_status>/', views.filtered_orders, name='filtered-orders'),
    path('order-management/update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('payment-management/', views.payment_management, name='payment-management'),
    path('payment-management/search/', views.payment_search, name='payment-search'),

    path('banner-management/', views.banner_management, name='banner-management'),

    path('coupon-management/', views.coupon_management, name='coupon-management'),
    path('coupon-management/add-coupon/', views.add_coupon, name='add-coupon'),
    path('coupon-management/delete-coupon/<str:pk>/', views.delete_coupon, name='delete-coupon'),
    path('coupon-management/edit-coupon/<str:pk>/', views.edit_coupon, name='edit-coupon'),
    
]