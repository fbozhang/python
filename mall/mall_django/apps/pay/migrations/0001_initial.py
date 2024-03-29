# Generated by Django 4.0.5 on 2022-09-25 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新時間')),
                ('trade_id', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='支付编号')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderinfo', verbose_name='订单')),
            ],
            options={
                'verbose_name': '支付信息',
                'verbose_name_plural': '支付信息',
                'db_table': 'tb_payment',
            },
        ),
    ]
