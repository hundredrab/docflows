from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Document, Permission
from account.models import User, Committee, Role, Member


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
        u1 = User.objects.create(username='user11')
        u2 = User.objects.create(username='user22')
        c1 = Committee.objects.create(name='comm1', description='Test Comm.')
        r1 = Role.objects.create(
            name='Member', committee=c1, description='New role.')
        m1 = Member.objects.create(user=u1, role=r1)
        # print([d1,d2,d3,u1,u2,c1,r1,m1])

        p1 = Permission.objects.create(document=d1, holder=u1, name='1')
        p2 = Permission.objects.create(document=d2, holder=r1, name='1')
        p3 = Permission.objects.create(document=d2, holder=u2, name='2')
        p4 = Permission.objects.create(document=d1, holder=c1, name='3')
