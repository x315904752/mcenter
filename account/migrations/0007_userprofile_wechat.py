# Generated by Django 2.0 on 2018-01-29 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180124_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wechat',
            field=models.CharField(blank=True, max_length=64, verbose_name='微信号'),
        ),
    ]
