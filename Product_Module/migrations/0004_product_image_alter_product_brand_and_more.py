# Generated by Django 4.2.2 on 2023-09-20 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product_Module', '0003_productbrand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product_Module.productbrand', verbose_name='برند'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='title',
            field=models.CharField(db_index=True, max_length=300, verbose_name='نام برند'),
        ),
    ]