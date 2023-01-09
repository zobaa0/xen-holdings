from .models import Referral
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

user = get_user_model()

@receiver(post_save, sender=user)
def create_referral(sender, instance, created, *args, **kwargs):
    if created:
        Referral.objects.create(user=instance)