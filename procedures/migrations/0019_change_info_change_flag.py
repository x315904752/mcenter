# Generated by Django 2.0 on 2018-01-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0018_auto_20180123_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='change_info',
            name='change_flag',
            field=models.IntegerField(default=None, verbose_name='变更状态'),
        ),
    ]