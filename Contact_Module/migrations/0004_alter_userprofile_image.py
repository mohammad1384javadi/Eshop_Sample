# Generated by Django 4.2.2 on 2023-08-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contact_Module', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
