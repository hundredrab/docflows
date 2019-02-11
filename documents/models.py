import os
from distutils.core import extension_keywords

from django.contrib.auth.models import User as AuthUser
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import get_random_string
from taggit.managers import TaggableManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/YYYY/MM/DD/<random_strings.{extension for identifying file to open}>
    def extension(filename):
        name, ext = os.path.splitext(filename)
        return ext
    ext = extension(filename)
    return '{0}/{1}/{2}'.format('documents', timezone.now().strftime("%Y/%m/%d"), get_random_string(30)+ext)


class Document(models.Model):
    """Documents and associated information."""

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        'account.User', null=True, blank=True, on_delete=models.CASCADE)
    tags = TaggableManager()
    file = models.FileField(upload_to=user_directory_path)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def shareable_by(self, user):
        """Check if the user can share the doc."""

        query = ((Q(permission__user_permits=user) | Q(permission__comm_permits__com_roles__member__user=user) | Q(permission__role_permits__member__user=user)) & Q(permission__level=1) & Q(permission__document = self))
        perms = Document.objects.filter(query).count()
        print(perms)
        if perms:
            return True
        else:
            return False

    def viewable_by(self, user):
        """Check if the user can view the doc."""

        query = (Q(permission__user_permits=user) | Q(permission__comm_permits__com_roles__member__user=user) | Q(permission__role_permits__member__user=user)) & Q(permission__document = self)
        perms = Document.objects.filter(query).count()
        print(perms)
        if perms:
            return True
        else:
            return False


class Permission(models.Model):
    """Permissions associated with documents.

    Has a generic 'holder' relation which should be mapped to a Role, a Committee,
    or an User.
    """

    PERMISSION_CHOICES = ((0, 'VIEW'), (1, 'SHARE'))

    level = models.PositiveIntegerField(choices=PERMISSION_CHOICES)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='permits')
    object_id = models.PositiveIntegerField()
    holder = GenericForeignKey('content_type', 'object_id')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
