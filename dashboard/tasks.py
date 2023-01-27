from rsfholdings.celery import app
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rsfholdings import settings
from datetime import date as dt


@app.task
def activate_subscription(instance_id):
    """
    Task to automatically calculate and add daily profit
    to each user with an active plan.
    """
    # GLOBAL IMPORTS
    from dashboard.models import Subscription, Plan

    # CELERY IMPORTS
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    # GET THE SUBSCRIPTION, PLAN % USER INSTANCE
    instance = get_object_or_404(Subscription, id=instance_id)
    plan = get_object_or_404(Plan, id=instance.plan_id)
    user = instance.user

    # calculate the interest based on the plan's interest rate
    interest = instance.sub_amount * (plan.percent / plan.calc_percent)

    # Check if the plan has expired
    if instance.expires_at < dt.today():
        # If the plan has expired, delete any existing
        # periodic tasks for this deposit
        PeriodicTask.objects.filter(args=[instance_id]).delete()
    else:
        # If the plan has not expired, create
        # a new periodic task
        if dt.today() == instance.verified_on:
            # If the plan was activated today,
            # do nothing.
            pass
        elif dt.today() < instance.expires_at:
            # If the plan is yet to expire, update
            # the user's bal and profit.
            user.balance = F('balance') + interest
            user.profit = F('profit') + interest
            user.save()
        elif dt.today() == instance.expires_at:
            # If the plan is expiring today, update user's
            # bal, profit & subscription amount.
            user.balance = F('balance') + interest + instance.sub_amount
            user.profit = F('profit') + interest
            user.save()
            Subscription.objects.filter(pk=instance_id).update(
                status='Expired',
            )

            # TODO: send confirmation email to user
            context = ({
                'user': user.username,
                'amount': instance.sub_amount,
                'plan': plan.plan_name,
                'percent': plan.percent,
                'duration': plan.duration
            })
            html_version = './dashboard/mails/completed_dep.html'
            html_message = render_to_string(html_version, context)
            subject = 'siteName - Investment Completed'
            message = EmailMessage(subject, html_message,
                                   settings.EMAIL_HOST_USER, [user.email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)

        else:
            pass

    # Create a periodic task to run the activate_subscription
    # task everyday
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    periodic_task, created = PeriodicTask.objects.get_or_create(
        interval=schedule,
        name=f"Update balance and profit for subscription {instance_id}",
        task="dashboard.tasks.activate_subscription", args=[instance_id],
    )
