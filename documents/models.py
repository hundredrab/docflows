from django.utils import timezone
from distutils.core import extension_keywords

from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.crypto import get_random_string

from account import models as acc_m


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}'.format('documents', timezone.now().strftime("%Y/%m/%d"), get_random_string(30))


class Document(models.Model):
    """Documents and associated information."""

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    #keywords = 
    #subject = 
    file = models.FileField(upload_to=user_directory_path)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' (' + self.description[:15] + '...)'


class Permission(models.Model):
    """Permissions associated with documents.

    Has a generic 'holder' relation which should be mapped to a Role, a Committee,
    or an User.
    """

    PERMISSION_CHOICES = ((0, 'VIEW'), (1, 'SHARE'))

    level = models.CharField(max_length=10, choices=PERMISSION_CHOICES)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='permits')
    object_id = models.PositiveIntegerField()
    holder = GenericForeignKey('content_type', 'object_id')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
