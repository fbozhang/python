# Generated by Django 4.0.5 on 2022-09-10 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PAuthQQUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新時間')),
                ('openid', models.CharField(db_index=True, max_length=64, verbose_name='openid')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用戶')),
            ],
            options={
                'verbose_name': 'QQ登錄用戶數據',
                'verbose_name_plural': 'QQ登錄用戶數據',
                'db_table': 'tb_oauth_qq',
            },
        ),
    ]