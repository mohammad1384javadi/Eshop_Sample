# Generated by Django 4.2.2 on 2023-10-06 13:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Article_Module', '0002_articlecomments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticleComments',
            new_name='ArticleComment',
        ),
    ]