from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from .models import User


@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, **kwargs):
    User.objects.get_or_create(user=instance, defaults={
                               'username': instance.username})
