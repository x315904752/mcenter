# Generated by Django 2.0 on 2018-01-24 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0028_auto_20180124_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='change_next_people',
            name='next_persion',
        ),
    ]
