# Generated by Django 2.1.4 on 2019-02-06 08:12

from django.db import migrations, models
import django.db.models.deletion
import documents.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to=documents.models.user_directory_path)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.User')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField(choices=[(0, 'VIEW'), (1, 'SHARE')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permits', to='contenttypes.ContentType')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Document')),
            ],
        ),
    ]
