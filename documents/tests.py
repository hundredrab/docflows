from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from account.models import Committee, Member, Role, User
from django.contrib.auth.models import User as AuthUser

from .models import Document, Permission

client = APIClient()


class Test_Docs(TestCase):
    """Test module for testing documents and permission related views."""

    def setUp(self):
        doc_file = SimpleUploadedFile("test.txt", b"This is a test file.")

        d1 = Document.objects.create(name="Test doc1",
                                     description="",
                                     file=doc_file)
        d2 = Document.objects.create(name="Test doc2",
                                     description="",
                                     file=doc_file)
        d3 = Document.objects.create(name="Test doc3",
                                     description="",
                                     file=doc_file)
        ua1 = AuthUser.objects.create(
            username='authuser1', password='pass@123456789')
        ua2 = AuthUser.objects.create(
            username='authuser2', password='pass@123456789')
        ua3 = AuthUser.objects.create(
            username='authuser3', password='pass@123456789')
        u1 = ua1.user_prof
        u2 = ua2.user_prof
        u3 = ua3.user_prof
        c1 = Committee.objects.create(name='comm1', description='Test Comm.', owner=u1)
        r1 = Role.objects.create(
            name='Member', committee=c1, description='New role.')
        m1 = Member.objects.create(user=u1, role=r1)
        # print([d1,d2,d3,u1,u2,c1,r1,m1])

        p1 = Permission.objects.create(document=d1, holder=u1, level=0)
        p2 = Permission.objects.create(document=d2, holder=r1, level=1)
        p3 = Permission.objects.create(document=d2, holder=u2, level=1)
        p4 = Permission.objects.create(document=d1, holder=c1, level=1)

        # Permissions:
        # d1: read: u1
            # share: u1(r1,c1)
        # d2: share: u1, u2

    def test_correct_permissions_are_retrieved(self):
        d1 = Document.objects.get(name="Test doc1")
        d2 = Document.objects.get(name="Test doc2")
        u1 = AuthUser.objects.get(username='authuser1').user_prof
        u2 = AuthUser.objects.get(username='authuser2').user_prof
        u3 = AuthUser.objects.get(username='authuser3').user_prof
        assert d1.shareable_by(u1)
        assert not d1.shareable_by(u2)
        assert d2.shareable_by(u2)
        assert d2.viewable_by(u1)

        assert not d2.viewable_by(u3)
