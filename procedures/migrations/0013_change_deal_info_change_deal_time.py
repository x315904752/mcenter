# Generated by Django 2.0 on 2018-01-22 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0012_auto_20180119_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='change_deal_info',
            name='change_deal_time',
            field=models.DateTimeField(default=None, verbose_name='处理时间'),
        ),
    ]
