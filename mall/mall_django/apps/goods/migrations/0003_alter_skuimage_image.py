# Generated by Django 4.0.5 on 2023-03-28 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_alter_brand_id_alter_goodscategory_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skuimage',
            name='image',
            field=models.ImageField(upload_to='sku/', verbose_name='图片'),
        ),
    ]