from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from portal.models import Settings

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user(sender, instance, created, **kwargs):
    try:
        instance.settings
    except Settings.DoesNotExist:
        Settings.objects.create(user=instance)
