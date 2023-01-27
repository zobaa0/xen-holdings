from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Subscription, Withdrawal, Transfer
from rsfholdings import settings

from datetime import timedelta, date as dt


@receiver(post_save, sender=Subscription)
def update_subscription(sender, instance, *args, **kwargs):
    if instance.active == True:
        Subscription.objects.filter(id=instance.id).update(
            status="Confirmed", verified_on=dt.today(),
            # TODO: Case-scenario where the user has multiple deposit plans
            expires_at=dt.today() + timedelta(days=instance.plan.duration),
        )


@receiver(post_save, sender=Withdrawal)
def verify_withdrawal(sender, instance, *args, **kwargs):
    if instance.status == 'Confirmed':
        Withdrawal.objects.filter(pk=instance.pk).update(
            verified_on=timezone.now(),
        )


@receiver(post_save, sender=Transfer)
def verify_transfer(sender, instance, *args, **kwargs):
    user = instance.user
    if instance.status == 'Confirmed':
        Transfer.objects.filter(pk=instance.pk).update(
            verified_on=timezone.now(),
        )
    # TODO: send confirmation email to user
        context = ({
            'user': user.username,
            'amount': instance.amount,
            'receiver': instance.username,
        })
        html_version = './dashboard/mails/active_tf.html'
        html_message = render_to_string(html_version, context)
        subject = 'siteName - Transfer Approved'
        message = EmailMessage(subject, html_message,
                               settings.EMAIL_HOST_USER, [user.email])
        message.content_subtype = 'html'
        message.send(fail_silently=True)


# @receiver(post_save, sender=Subscription)
# def confirm_plan_closure(sender, instance, **kwargs):
#     user = instance.user
#     if instance.status == 'Expired':
#         # TODO: send confirmation email to user
#         context = ({
#             'user': user.username,
#             'amount': instance.sub_amount,
#             'plan': instance.plan.plan_name,
#             'percent': instance.plan.percent,
#             'duration': instance.plan.duration
#         })
#         html_version = './dashboard/mails/completed_dep.html'
#         html_message = render_to_string(html_version, context)
#         subject = 'siteName - Investment Completed'
#         message = EmailMessage(subject, html_message,
#                                settings.EMAIL_HOST_USER, [user.email])
#         message.content_subtype = 'html'
#         message.send(fail_silently=True)
