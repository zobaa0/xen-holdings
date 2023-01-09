from django.contrib import admin
from .models import CustomUser, Referral
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    '''Admin View for CustomUser'''

    list_display = ('email', 'first_name', 'last_name', 'balance', 'profit')
    list_filter = ('username', 'email')
    readonly_fields = ('otp_base32', 'otp_auth_url', 'date_joined',
                       'last_login', 'del_account_due_date', 'country', 
                       'state', 'phone', 'first_name', 'last_name', 'address')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    fieldsets = (
        ('BASIC INFO', {
            'fields': (
                'username', 'email', 'password', 'terms'
            ),
        }),
        ('KYC', {
            'fields': (
                'first_name', 'last_name', 'country', 'state', 'address', 'phone'
            ),
        }),
        ('BALANCE', {
            'fields': (
                'balance', 'profit'
            ),
        }),
        ('ACCOUNT STATUS', {
            'fields': (
                'date_joined', 'last_login', 'is_active',
            ),
        }),
        ('2FA AUTH', {
            'fields': (
                'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url'
            ),
        }),
        ('ACTIVATE TRANSFER', {
            'fields': (
                'tf_enabled',
            ),
        }),
        ('DELETE ACCOUNT', {
            'fields': (
                'del_account', 'deactivation_duration', 'del_account_due_date'
            ),
        }),
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    '''Admin View for Referral'''

    list_display = ('user', 'bonus', 'code', 'recommended_by')
    list_filter = ('user',)

    readonly_fields = ('code', 'recommended_by', 'user')
    search_fields = ('user__firstname', 'user__lastname', 'user__lastname')

    ordering = ('-user__date_joined',)
    fieldsets = (
        ('USER', {
            'fields': (
                'user', 'bonus', 'code'
            ),
        }),
        ('RECOMMENDER', {
            'fields': (
                'recommended_by',
            ),
        }),
    )
