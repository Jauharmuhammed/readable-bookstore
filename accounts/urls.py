from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name="login"),  
	  path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name='register'),

    path('activate/<uidb64>/<token>/', views.user_activate, name='activate'),

    path('login/login-with-otp', views.login_with_otp, name='login-with-otp'),
    path('login/login-with-otp/verify', views.login_with_otp_verify, name='login-with-otp-verify'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('forgot-password/verify/<uidb64>/<token>/', views.forgot_password_verify, name='forgot-password-verify'),
    path('reset-password/', views.reset_password, name='reset-password'),

]