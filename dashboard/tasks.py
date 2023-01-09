from celery import shared_task
from django.shortcuts import get_object_or_404
from django.db.models import F
from datetime import date as dt


@shared_task
def activate_subscription(instance_id):
    """
    Task to automatically calculate and add daily profit
    to each user with an active plan.
    """
    # GLOBAL IMPORTS
    from dashboard.models import Subscription, Plan

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
            instance.status = 'Expired'
            user.save()
        else:
            pass

    # Create a periodic task to run the activate_subscription
    # task everyday
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    periodic_task, created = PeriodicTask.objects.get_or_create(
        interval=schedule,
        name=f"Update balance and profit for subscription {instance_id}",
        task="dashboard.tasks.activate_subscription", args=[instance_id],
    )