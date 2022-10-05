from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name="login"),  
	  path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name='register'),

    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<uidb64>/', views.unsubscribe, name='unsubscribe'),

    path('activate/<uidb64>/<token>/', views.user_activate, name='activate'),

    path('login/login-with-otp', views.login_with_otp, name='login-with-otp'),
    path('login/login-with-otp/verify', views.login_with_otp_verify, name='login-with-otp-verify'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('forgot-password/verify/<uidb64>/<token>/', views.forgot_password_verify, name='forgot-password-verify'),
    path('reset-password/', views.reset_password, name='reset-password'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wislist/add-to-wislist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wislist/remove-from-wislist/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),

    path('dashboard/', views.dashboard, name='user-dashboard'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/edit-profile', views.edit_profile, name='edit-profile'),
    path('profile/change-password', views.change_password, name='change-password'),

    path('orders/', views.orders, name='user-orders'),
    path('orders/<str:order_id>/', views.order_details, name='user-order-details'),
    path('orders/cancel-order/<int:id>/', views.cancel_order, name='user-order-cancel'),
    path('orders/return-order/<int:id>/', views.return_order, name='user-order-return'),

    path('address/', views.address, name='user-address'),
    path('address/add-new-address', views.add_new_address, name='add-new-address'),
    path('address/delete-address/<int:address_id>/', views.delete_address, name='delete-address'),
    path('address/edit-address/<int:address_id>/', views.edit_address, name='edit-address'),

]