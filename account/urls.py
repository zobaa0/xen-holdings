from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('signup/<str:ref_code>/', register, name="register"),
    path('signup/', register, name="register"),
    path('login/', login_request, name="login"), 
    path('dashboard/password-change/', security, name="security"),
    path('forgot_password/', reset_password, name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html/', success_url='/account/login/'), name='password_reset_confirm'),
    path('generate_OTP/', generateOTP, name='generate_OTP'),
    path('verify_OTP/', verifyOTP, name='verify_OTP'),
    path('login/validate_OTP/', validateOTP, name='validate_OTP'),
    path('disable_OTP', disableOTP, name='disable_OTP')
]