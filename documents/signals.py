from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, Permission

@receiver(post_save, sender=Document)
def create_permission(sender, **kwargs):
	# Doc = Document.objects.get(id=kwargs['instance'])
	if kwargs['created']:
		per = Permission.objects.create(document=kwargs['instance'], object_id=1, level=1, content_type=4)
		# per.object_id = 1
		# per.level = 1
		# per.content_type = 4 ##for user
		# per.save(update_fields=['object_id','level','content_type'])

# @receiver(post_save, sender=Document)
# def save_premissions(sender, **kwargs):
# 	p = kwargs['instance']
# 	p.level = 1
# 	p.content_type = 4 ##4=user
# 	p.object_id = 1
# 	p.save()
	