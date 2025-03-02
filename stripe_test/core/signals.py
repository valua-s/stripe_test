from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from .models import Order


@receiver(post_save, sender=Order)
def create_username_and_password(sender, instance: Order, created, **kwargs):

    if created:
        instance.unique_code = uuid.uuid4()
        instance.save()
        