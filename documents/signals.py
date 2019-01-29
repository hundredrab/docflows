from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, Permission

@receiver(post_save, sender=Document)
def create_permission(sender, **kwargs):
	if kwargs['created']:
		per = Permission.objects.create(document=kwargs['instance'], level=1, holder=kwargs['instance'].owner)
	