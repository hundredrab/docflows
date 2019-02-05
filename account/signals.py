from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, **kwargs):
    User.objects.get_or_create(user=instance, defaults={
                               'username': instance.username})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
