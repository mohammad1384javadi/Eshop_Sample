# Generated by Django 4.2.2 on 2023-11-09 17:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Article_Module', '0004_articlescomment_delete_articlecomment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticlesComment',
            new_name='ArticleComments',
        ),
    ]
