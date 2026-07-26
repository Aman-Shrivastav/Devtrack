import secrets

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company


@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Company profile whenever
    a new Django User is created.
    """

    if created:
        Company.objects.create(
            user=instance,
            company_name=instance.username,   # Temporary value
            api_key=secrets.token_urlsafe(32)
        )