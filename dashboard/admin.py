from django.contrib import admin
from .models import Plan, Subscription, Withdrawal, Wallet, MinimumAmount, Transfer


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    '''Admin View for Plan'''

    list_display = ('plan_name', 'min', 'max', 'percent', 'duration')
    fieldsets = (
        ('INVESTMENT PLAN', {
            'fields': (
                'plan_name', 'min', 'max', 'percent', 'duration'
            ),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    '''Admin View for Subscription'''

    list_display = ('user', 'plan', 'sub_method',
                    'sub_currency', 'sub_amount', 'status', 'active')
    list_filter = ('active', 'status', 'plan')
    readonly_fields = ('expires_at', 'initiated_on', 'verified_on',
                       'status', 'user', 'sub_currency', 'sub_method')
    search_fields = ('user', 'plan', 'status', 'sub_currency')
    date_hierarchy = 'verified_on'
    ordering = ('-initiated_on',)
    fieldsets = (
        ('USER', {
            'fields': (
                'user',
            ),
        }),
        ('SUBSCRIPTION DETAILS', {
            'fields': (
                'plan', 'sub_amount', 'sub_method', 'sub_currency'
            ),
        }),
        ('DATES', {
            'fields': (
                'initiated_on', 'verified_on', 'expires_at'
            ),
        }),
        ('ACTIVATE SUBSCRIPTION', {
            'fields': (
                'active', 'status'
            ),
        }),
    )


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    '''Admin View for Withdrawal'''

    list_display = ('user', 'amount', 'wallet', 'status')
    list_filter = ('status', 'wallet')
    readonly_fields = ('initiated_on', 'verified_on', 'wallet', 'user')
    search_fields = ('user',)
    date_hierarchy = 'verified_on'
    ordering = ('-initiated_on',)
    fieldsets = (
        ('USER', {
            'fields': (
                'user',
            ),
        }),
        ('WITHDRAWAL DETAILS', {
            'fields': (
                'amount', 'wallet'
            ),
        }),
        ('DATES', {
            'fields': (
                'initiated_on', 'verified_on'
            ),
        }),
        ('VERIFY WITHDRAWAL', {
            'fields': (
                'status',
            ),
        }),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    '''Admin View for Wallet'''

    list_display = ('user', 'type', 'address')
    list_filter = ('type',)
    readonly_fields = ('user', 'type', 'address')
    search_fields = ('user', 'type')
    fieldsets = (
        ('WALLET ADDRESS DETAILS', {
            'fields': (
                'user', 'type', 'address'
            ),
        }),
    )


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    '''Admin View for Transfer'''

    list_display = ('user', 'amount', 'username', 'status')
    list_filter = ('status',)
    readonly_fields = ('initiated_on', 'verified_on', 'user', 'username')
    search_fields = ('user', 'username', 'amount')
    date_hierarchy = 'verified_on'
    ordering = ('-initiated_on',)
    fieldsets = (
        ('USER INITIATING TRANSFER', {
            'fields': (
                'user', 'amount'
            ),
        }),
        ('USER ACCEPTING TRANSFER', {
            'fields': (
                'username',
            ),
        }),
        ('DATES', {
            'fields': (
                'initiated_on', 'verified_on'
            ),
        }),
        ('VERIFY TRANSFER', {
            'fields': (
                'status',
            ),
        }),
    )


@admin.register(MinimumAmount)
class MinimumAmountAdmin(admin.ModelAdmin):
    '''Admin View for MinimumAmount'''

    list_display = ('min_withdraw', 'min_transfer')
    fieldsets = (
        ('MINIMUM WITHDRAWAL', {
            'fields': (
                'min_withdraw',
            ),
        }),
        ('MINIMUM TRANSFER', {
            'fields': (
                'min_transfer',
            ),
        }),
    )
