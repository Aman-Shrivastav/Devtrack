import secrets

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Company


@receiver(pre_save, sender=User)
def remember_new_user_state(sender, instance, **kwargs):
    """Capture Django's adding flag before save resets it."""
    instance._teamboard_user_is_new = instance._state.adding


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Company profile whenever
    a new Django User is created.
    """

    if getattr(instance, "_teamboard_user_is_new", False):
        Company.objects.create(
            user=instance,
            company_name=instance.username,   # Temporary value
            api_key=secrets.token_urlsafe(32)
        )
