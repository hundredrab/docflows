from django.db import models
from documents.models import Document


class Approval(models.Model):
    """Approval exit criteria for a node."""
    comment = models.TextField()
    status = models.CharField(max_length=10, default='Pending', choices=(('Pending', 'Pending'),
                                                                         ('Approved', 'Approved'),
                                                                         ('Rejected', 'Rejected')
                                                                         ))

class Node(models.Model):
    """A node is the most basic unit of a process. 

    Each node has either (and only one among) an approval, or a document upload,
    as its exit criteria.

    The document upload or process approval is atomic, and involves only one file,
    or one committee/user/role approval."""

    document = models.ForeignKey(Document, related_name='document_to_upload')
    # approval_required_for = models.ForeignKey(Document, related_name='approvals_required')
    approval = models.ForeignKey(Approval, related_name='approvals_required')

