from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from documents.models import Document


class Approval(models.Model):
    """Approval exit criteria for a node."""
    comment = models.TextField()
    status = models.CharField(max_length=10, default='Pending',
                              choices=(('pending', 'Pending'),
                                       ('approved', 'Approved'),
                                       ('rejected', 'Rejected')
                                       ))
    last_modified = models.DateTimeField(blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='approvals')
    object_id = models.PositiveIntegerField()
    approver = GenericForeignKey('content_type', 'object_id')


class DocumentRequirement(models.Model):
    """Document Required exit criteria for a node."""
    name = models.CharField(max_length=50)
    comment = models.TextField()
    document = models.ForeignKey(
        Document, on_delete=models.DO_NOTHING, blank=True, null=True)


class Process(models.Model):
    """A process is an instance of Flow, and represents a single real-life process.

    It is composed of multiple nodes.
    Flow could be stored in a file, separately, to allow reuse."""

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    current_node = models.DecimalField(
        default=1, max_digits=3, decimal_places=0)


class Node(models.Model):
    """A node is the most basic unit of a process.

    Each node has either (and only one among) an approval, or a document upload,
    as its exit criteria.

    The document upload or process approval is atomic, and involves only one file,
    or one committee/user/role approval."""

    name = models.CharField(default='1', max_length=3)
    document = models.ForeignKey(DocumentRequirement, related_name='document_to_upload', on_delete=models.CASCADE,
                                 blank=True, null=True)
    # TODO: Polymorphic relation for approval/document.
    approval = models.ForeignKey(Approval, related_name='approvals_required', on_delete=models.CASCADE,
                                 blank=True, null=True)
    process = models.ForeignKey(
        Process, related_name='node', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'process')
