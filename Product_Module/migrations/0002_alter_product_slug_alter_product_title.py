# Generated by Django 4.2.2 on 2023-07-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_Module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=200, unique=True, verbose_name='عنوان در url'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=300, verbose_name='نام محصول'),
        ),
    ]
