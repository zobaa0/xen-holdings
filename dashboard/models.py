from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.db.models import F
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import re

from rsfholdings import settings
from dashboard.tasks import activate_subscription

# Custom user
user = get_user_model()


class Plan(models.Model):
    plan_name = models.CharField(max_length=70, verbose_name='Plan')
    percent = models.PositiveIntegerField(verbose_name='Interest rate')
    ref_bonus = models.PositiveIntegerField(default=10, verbose_name='Referral bonus')
    min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Minimum deposit')
    max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Maximum deposit')
    calc_percent = models.DecimalField(
        max_digits=10, editable=False, decimal_places=2, default=100.00, verbose_name='Percentage Formula')
    duration = models.PositiveIntegerField(verbose_name='Plan duration')

    def __str__(self):
        return self.plan_name


class Subscription(models.Model):
    SUB_METHOD = (
        ('Account', 'Account Balance'),
        ('Wallet', 'Wallet')
    )
    SUB_CURRENCY = (
        ('Btc', 'Bitcoin - BTC'),
        ('Eth', 'Ethereum - ETH'),
        ('Trc20', 'Tether - USDT(TRC20)')
    )
    SUB_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Expired', 'Expired')
    )
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="user")
    type = models.CharField(max_length=10, default="Investment", editable=False)
    plan = models.ForeignKey(
        Plan, on_delete=models.DO_NOTHING, related_name="plan")
    sub_method = models.CharField(
        max_length=24, choices=SUB_METHOD, default='Account')
    sub_currency = models.CharField(
        max_length=12, choices=SUB_CURRENCY, default='Btc')
    sub_amount = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    expires_at = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=9, choices=SUB_STATUS, default="Pending")
    verified_on = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    initiated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Username: {self.user.username.capitalize()} - Balance: ${self.user.balance}"

    def clean(self):
        """SUBSCRIPTION CUSTOM VALIDATION"""
        # Don't allow amount out of the Basic plan range
        if self.plan.plan_name:
            if self.sub_amount < self.plan.min or self.sub_amount > self.plan.max:
                raise ValidationError({'sub_amount': _(
                    f"Enter an amount within the range of ${self.plan.min} and ${self.plan.max}")})
            # Validate Account Balance
            if self.sub_method == "Account":
                if self.sub_amount > self.user.balance:
                    raise ValidationError(
                        {'sub_amount': _(f"Insufficient balance. Kindly recharge via your wallet")})

    @classmethod
    def update_active_bal(cls, sender, instance, *args, **kwargs):
        """Update user account bal. after payment confirmation"""
        user = instance.user
        if instance.sub_method == "Account":
            user.balance = F('balance') - instance.sub_amount
            user.save()

    @classmethod
    def activate_subscription(cls, sender, instance, *args, **kwargs):
        """Start the countdown"""
        user = instance.user
        if instance.active:
            # TODO: SEND CONFIRMATION MAIL
            context = ({
                'user': user.username,
            })
            html_version = './dashboard/mails/active_dep.html'
            html_message = render_to_string(html_version, context)
            subject = 'siteName - Investment Package Activated'
            message = EmailMessage(subject, html_message,
                                   settings.EMAIL_HOST_USER, [user.email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)

            # Let celery handle the logic asynchronously
            transaction.on_commit(
                lambda: activate_subscription.apply_async(args=(instance.pk,)))


post_save.connect(Subscription.update_active_bal, sender=Subscription)
post_save.connect(Subscription.activate_subscription, sender=Subscription)


class Wallet(models.Model):
    NETWORK = (
        ('Btc', 'Bitcoin - BTC'),
        ('Eth', 'Ethereum - ETH'),
        ('Trc20', 'Tether - USDT(TRC20)')
    )
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20, choices=NETWORK, verbose_name="Wallet name")
    address = models.CharField(max_length=60, verbose_name="Wallet address")

    class Meta:
        verbose_name_plural = 'Wallet Address'
        unique_together = ('user', 'type')

    def __str__(self):
        return f"{self.get_type_display()}"


class MinimumAmount(models.Model):
    """Model definition for MinimumAmount."""

    # TODO: Define fields here
    min_withdraw = models.DecimalField(
        default=0.00, max_digits=1000, decimal_places=2, verbose_name='Minimum Withdrawal Amount')
    min_transfer = models.DecimalField(
        default=0.00, max_digits=1000, decimal_places=2, verbose_name='Minimum Transfer Amount')

    class Meta:
        """Meta definition for MinimumAmount."""

        verbose_name_plural = 'Minimum Withdrawal & Transfer'

    def __str__(self):
        """Unicode representation of MinimumAmount."""
        return f'Minimum'


class Withdrawal(models.Model):
    WITHDRAW_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    )
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.SET_NULL, null=True, verbose_name="Withdrawal wallet")
    minimum = models.ForeignKey(MinimumAmount, on_delete=models.SET_DEFAULT, default=1)
    type = models.CharField(
        max_length=10, default="Withdrawal", editable=False)
    amount = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00, verbose_name="Withdrawal amount")
    status = models.CharField(max_length=12, choices=WITHDRAW_STATUS,
                              default="Pending", verbose_name="Withdrawal status")
    verified_on = models.DateTimeField(blank=True, null=True)
    initiated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Username: {self.user.username.capitalize()} - Balance: ${self.user.balance}"

    def clean(self):
        """WITHDRAWAL CUSTOM VALIDATION"""
        if self.amount > self.user.balance:
            raise ValidationError(
                {'amount': _(f"Withdrawal failed! Insufficient balance.")})
        if self.amount < self.minimum.min_withdraw:
            raise ValidationError({'amount': _(
                f"Withdrawal failed! Minimum withdrawal amount is ${self.minimum.min_withdraw}.")})

    @classmethod
    def confirm_withdrawal(cls, sender, instance, *args, **kwargs):
        """
        Update user account bal. after payment confirmation
        and send confirmation mail to the user
        """
        user = instance.user
        if instance.status == "Confirmed":
            user.balance = F('balance') - instance.amount
            user.save()
            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({
                'user': user.username,
                'amount': instance.amount,
                'wallet': instance.wallet.type,
                'address': instance.wallet.address
            })
            html_version = './dashboard/mails/active_with.html'
            html_message = render_to_string(html_version, context)
            subject = 'siteName - Withdrawal Approved'
            message = EmailMessage(subject, html_message,
                                   settings.EMAIL_HOST_USER, [user.email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)


post_save.connect(Withdrawal.confirm_withdrawal, sender=Withdrawal)


class Transfer(models.Model):
    """Model definition for Transfer."""

    TRANSFER_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed')
    )

    # TODO: Define fields here
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    minimum = models.ForeignKey(
        MinimumAmount, on_delete=models.SET_DEFAULT, default=1)
    username = models.CharField(max_length=50, verbose_name='Transfer to')
    amount = models.DecimalField(
        max_digits=1000, decimal_places=2, verbose_name='Transfer amount')
    status = models.CharField(max_length=50, choices=TRANSFER_STATUS,
                              default='Pending', verbose_name='Transfer status')
    initiated_on = models.DateTimeField(auto_now_add=True)
    verified_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Unicode representation of Transfer."""
        return self.user.username

    def clean(self):
        """TRANSFER CUSTOM VALIDATION"""
        if not self.user.tf_enabled:
            raise ValidationError(
                _(f"You are not approved for transfer. Contact support."))
        if not (self.username and user.objects.filter(username__iexact=self.username).exists()):
            raise ValidationError(
                {'username': _(f"Transfer failed! User does not exist.")})
        if self.amount < self.minimum.min_transfer:
            raise ValidationError(
                {'amount': _(f"Transfer failed! Minimum transfer amount is {self.minimum.min_transfer}.")})
        if self.amount > self.user.balance:
            raise ValidationError(
                {'amount': _(f"Transfer failed! Insufficient account balance.")})

    @classmethod
    def confirm_transfer(cls, sender, instance, *args, **kwargs):
        """
        Debit sender's account balance after confirmation, credit
        the recipient and send confirmation mail.
        """
        sender = instance.user
        recipient = instance.username

        if instance.status == 'Confirmed':
            # Retrieve recipient's details
            recipient = user.objects.get(username__iexact=recipient)
            # Debit user
            sender.balance = F('balance') - instance.amount
            # Credit recipient
            recipient.balance = F('balance') + instance.amount
            # Update user's balance
            sender.save()
            # Update recipient's balance
            recipient.save()
            # TODO: Send confirmation mail to the sender & user


post_save.connect(Transfer.confirm_transfer, sender=Transfer)