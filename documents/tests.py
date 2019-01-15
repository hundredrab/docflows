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
            username='authuser1', PASSWORD='pass@123456789')
        ua2 = AuthUser.objects.create(
            username='authuser2', PASSWORD='pass@123456789')
        u1 = User.objects.create(username='user11', user=ua1)
        u2 = User.objects.create(username='user22', user=ua2)
        c1 = Committee.objects.create(name='comm1', description='Test Comm.')
        r1 = Role.objects.create(
            name='Member', committee=c1, description='New role.')
        m1 = Member.objects.create(user=u1, role=r1)
        # print([d1,d2,d3,u1,u2,c1,r1,m1])

        p1 = Permission.objects.create(document=d1, holder=u1, name=0)
        p2 = Permission.objects.create(document=d2, holder=r1, name=1)
        p3 = Permission.objects.create(document=d2, holder=u2, name=1)
        p4 = Permission.objects.create(document=d1, holder=c1, name=1)
